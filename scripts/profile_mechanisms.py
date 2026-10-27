"""Project-specific profile compositions. Source-derived illustrations, not executions."""
import hashlib
import json
import math
import struct


class Diagram:
    def __init__(self, root, project, roles, fonts, narrow, height=1100):
        import matplotlib.pyplot as plt
        self.plt, self.root, self.project = plt, root, project
        self.roles, self.fonts, self.narrow = roles, fonts, narrow
        self.w, self.h = (960 if narrow else 1800), height
        self.fig = plt.figure(figsize=(self.w / 100, self.h / 100), dpi=100,
                              facecolor=roles['canvas'])
        self.ax = self.fig.add_axes((0, 0, 1, 1), xlim=(0, self.w), ylim=(self.h, 0))
        self.ax.axis('off')
        self.labels, self.shapes = [], []
        self.size = 48 if narrow else 40
        self.text(60, 30, project['title'], 56 if narrow else 54, 'Bold', width=self.w-120)
        self.top = self.bottom + 35
        self.text(60, self.top, project['composition'].upper(), 30, 'SemiBold',
                  'accent', width=self.w-120)
        self.top = self.bottom + 60

    @property
    def bottom(self):
        return max((r['bounds'][3] for r in self.labels), default=0)

    def text(self, x, y, value, size=None, face='Regular', role='text', width=None):
        size = size or self.size
        label = self.ax.text(x, y, value, fontproperties=self.fonts[face](size),
                             va='top', color=self.roles[role], linespacing=1.18, zorder=5)
        self.fig.canvas.draw()
        if width:
            lines = []
            for paragraph in value.split('\n'):
                line = ''
                for word in paragraph.split():
                    candidate = (line+' '+word).strip()
                    label.set_text(candidate)
                    if label.get_window_extent(self.fig.canvas.get_renderer()).width <= width:
                        line = candidate
                    elif line:
                        lines.append(line); line = word
                        label.set_text(word)
                        if label.get_window_extent(self.fig.canvas.get_renderer()).width > width:
                            raise ValueError('Unbreakable label: '+word)
                    else:
                        raise ValueError('Unbreakable label: '+word)
                lines.append(line)
            label.set_text('\n'.join(lines))
        self.fig.canvas.draw()
        bounds = label.get_window_extent(self.fig.canvas.get_renderer())
        a = self.ax.transData.inverted().transform((bounds.x0, bounds.y1))
        b = self.ax.transData.inverted().transform((bounds.x1, bounds.y0))
        row = {'text': label.get_text(), 'size': size,
               'bounds': [float(a[0]), float(a[1]), float(b[0]), float(b[1])]}
        self.labels.append(row)
        return row['bounds'][3]

    def panel(self, x, y, w, h, *, dashed=False, fill='panel'):
        from matplotlib.patches import FancyBboxPatch
        self.ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0,rounding_size=12',
            facecolor=self.roles[fill],edgecolor=self.roles['border'],linewidth=2,
            linestyle='--' if dashed else '-',zorder=1))
        self.shapes.append([x,y,x+w,y+h])

    def line(self, a, b, *, dashed=False, role='border', lw=3, z=2):
        self.ax.plot([a[0],b[0]],[a[1],b[1]],color=self.roles[role],linewidth=lw,
                     linestyle='--' if dashed else '-',zorder=z)

    def arrow(self, a, b, *, dashed=False):
        from matplotlib.patches import FancyArrowPatch
        self.ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=25,
            color=self.roles['accent'],linewidth=2.5,linestyle='--' if dashed else '-',zorder=3))

    def circle(self, x, y, radius, *, fill='panel'):
        from matplotlib.patches import Circle
        self.ax.add_patch(Circle((x,y),radius,facecolor=self.roles[fill],
                                edgecolor=self.roles['border'],linewidth=2,zorder=2))
        self.shapes.append([x-radius,y-radius,x+radius,y+radius])

    def box(self, x, y, w, title, body='', *, h=150, dashed=False, size=None):
        self.panel(x,y,w,h,dashed=dashed)
        bottom=self.text(x+24,y+22,title,size or self.size,'SemiBold',width=w-48)
        if body:
            bottom=self.text(x+24,bottom+15,body,(size or self.size)-4,role='muted',width=w-48)
        if bottom>y+h-15:
            raise ValueError(self.project['id']+': box text overflow '+title+' actual='+str(bottom-y)+' limit='+str(h-15))
        return bottom

    def finish(self):
        content_bottom=max(self.bottom,max((s[3] for s in self.shapes),default=0))
        self.text(60,content_bottom+50,self.project['footer'],36 if self.narrow else 30,
                  role='muted',width=self.w-120)
        self.h=math.ceil(self.bottom+40)
        self.fig.set_size_inches(self.w/100,self.h/100,forward=False)
        self.ax.set_ylim(self.h,0)
        self.fig.canvas.draw()
        for row in self.labels:
            x0,y0,x1,y1=row['bounds']
            if x0<0 or y0<0 or x1>self.w or y1>self.h:
                raise ValueError(self.project['id']+': canvas overflow '+row['text'])
        name=self.root/'assets/explainers'/f"{self.project['id']}-obscur-{'narrow' if self.narrow else 'wide'}"
        metadata={'project':self.project,'kind':self.project['figure_class'],
                  'new_project_execution':False}
        self.fig.savefig(name.with_suffix('.png'),facecolor=self.roles['canvas'],
                         metadata={'Description':json.dumps(metadata,sort_keys=True)})
        with name.with_suffix('.svg').open('wb') as stream:
            self.fig.savefig(stream,format='svg',facecolor=self.roles['canvas'],
                             metadata={'Description':json.dumps(metadata,sort_keys=True),'Date':None})
        svg=name.with_suffix('.svg');svg.write_bytes(svg.read_bytes().replace(b'\r\n',b'\n'))
        self.plt.close(self.fig)
        return {'width':self.w,'height':self.h,'composition':self.project['composition'],
                'labels':self.labels,'shapes':self.shapes,'main_label_pixels':self.size,
                'kind':self.project['figure_class'],'new_project_execution':False}


def runtime(d):
    y=d.top
    d.text(60,y,'Ordinary uncancelled sum',face='SemiBold');y+=85
    x=230 if d.narrow else 330;cell=170
    d.text(60,y+20,'values',40)
    d.text(60,y+135,'mask',40)
    for i,(value,mask) in enumerate([(2,1),(-3,0),(5,1)]):
        d.panel(x+i*cell,y,140,95)
        d.text(x+35+i*cell,y+22,str(value),50,'SemiBold')
        d.panel(x+i*cell,y+115,140,95)
        d.text(x+40+i*cell,y+137,str(mask),50,'SemiBold')
        if not mask:d.line((x+i*cell+10,y+12),(x+i*cell+130,y+83),role='muted',lw=2)
    if d.narrow:
        d.arrow((480,y+230),(480,y+290));d.text(170,y+310,'2 + 5 = 7.0',66,'Bold')
        y+=465
    else:
        d.arrow((880,y+105),(1060,y+105));d.text(1120,y+75,'2 + 5 = 7.0',66,'Bold');y+=325
    d.text(60,y,'A separate ownership rule',face='SemiBold');y+=95
    left,right=100,d.w-100
    if d.narrow:
        d.panel(left,y+60,right-left,165)
        d.text(left+25,y+80,'Input + output storage\nstay owned',42,width=right-left-50)
        rail=y+280
        d.line((left,rail),(right,rail),role='accent')
        for xx in (left,(left+right)/2,right):
            d.line((xx,rail-30),(xx,rail+30),role='accent')
        for xx,label,width in ((60,'Admit',180),(350,'Cancel\nintent',230),(650,'Physical\nreturn',250)):
            d.text(xx,rail+55,label,38,width=width)
        d.text(60,rail+205,'Cancel intent does not end the storage lifetime.',42,width=840)
    else:
        d.panel(left,y+60,right-left,95)
        d.text(left+25,y+80,'Input and output storage stay owned',44,width=right-left-50)
        d.line((left,y+205),(right,y+205),role='accent')
        for xx,label in ((left,'Admit'),((left+right)/2,'Cancel intent'),(right,'Physical return')):
            d.line((xx,y+175),(xx,y+230),role='accent')
            d.text(max(60,min(xx-55,d.w-330)),y+250,label,40,width=310)
        d.text(60,y+355,'Cancel intent does not end the storage lifetime.',44,width=d.w-120)


def adaptive(d):
    y=d.top
    d.text(60,y,'Retained example: 101 requests',face='SemiBold',width=d.w-120);y+=100
    if d.narrow:
        d.text(60,y,'Physical computation',42,'SemiBold');y+=75
        d.box(60,y,840,'Payload 0 runs','New requests can replace waiting work.',h=270);y+=320
        d.box(250,y,650,'Waiting value: 100','99 waiting replacements.',h=220);y+=255
        d.arrow((130,y-225),(130,y+35))
        d.box(60,y+45,840,'Payload 0 returns','Obsolete result is rejected.',h=230);y+=300
        d.arrow((480,y-75),(480,y-10))
        d.box(60,y+15,840,'Payload 100 runs and returns','Physical completion is reconciled.',h=270);y+=330
        d.text(60,y,'Adoption gate: is this still current?',48,'Bold',width=840)
        d.box(60,d.bottom+45,840,'Adopt the current answer','Payload 100; revision 101.',h=250)
    else:
        labels=['Incoming requests','Physical work','Current answer']
        for i,label in enumerate(labels):
            yy=y+i*235;d.text(60,yy,label,40,'SemiBold',width=275)
            d.line((370,yy+45),(1700,yy+45),role='muted',z=0)
        d.box(420,y-10,450,'Payload 0 admitted',h=160,size=40)
        d.box(940,y-10,680,'Latest waiting value: 100',h=105,size=40)
        d.box(420,y+215,600,'Compute 0 -> return','Old result is rejected.',h=170,size=40)
        d.box(1120,y+215,565,'Compute 100 -> return',h=170,size=40)
        d.arrow((1020,y+300),(1100,y+300))
        d.box(1120,y+450,565,'Adopt revision 101','Payload 100 is the current answer.',h=240,size=40)
        d.arrow((1400,y+390),(1400,y+440))
        d.text(60,y+720,'2 computations; 99 waiting replacements; 1 obsolete result rejected.',38,
               width=d.w-120)


def atlas(d):
    y=d.top
    if d.narrow:
        d.text(60,y,'Source record -> observation',48,'SemiBold',width=840);y+=95
        px,pw=60,840
    else:
        d.box(60,y,590,'A credited source record','Locator, creator and inspection coverage.',h=240)
        d.arrow((650,y+120),(810,y+120))
        px,pw=850,890
    d.panel(px,y,pw,690)
    d.text(px+28,y+28,'Evidence passport',48,'Bold',width=pw-56)
    d.text(px+28,y+108,'Independent fields, not one verified badge',32,role='muted',width=pw-56)
    for i,label in enumerate(['Intake','Assertion','Time registration','Spatial registration','Availability','Rights']):
        yy=y+190+i*77
        d.text(px+28,yy,label,42,width=pw-290)
        d.line((px+pw-230,yy+25),(px+pw-35,yy+25),dashed=True)
    if not d.narrow:
        d.text(60,y+330,'Clock roles',46,'SemiBold')
        d.text(60,y+410,'Capture time\nPublication time\nPlayer-relative time',40,width=600)
        d.text(60,y+600,'A clock alone does not register a viewpoint.',38,role='muted',width=650)
    y+=750
    d.text(60,y,'Time and viewpoint may remain unknown.',44 if d.narrow else 46,
           'SemiBold',width=d.w-120);y=d.bottom+45
    if d.narrow:
        d.text(60,y,'Capture / publication / player clocks have different roles.',42,width=840);y=d.bottom+50
        d.box(60,y,840,'Documentary evidence','Inspect the source dossier and its limits.',h=280)
        d.box(60,y+330,840,'Procedural illustration','Labeled separately; not a source observation.',h=280,dashed=True)
    else:
        d.box(60,y,800,'Documentary evidence','Inspect the dossier and unresolved context.',h=280)
        d.box(940,y,800,'Procedural illustration','Separate, explicitly labeled layer.',h=280,dashed=True)


def shipment(d):
    y=d.top
    if d.narrow:
        left,right=90,870
        d.text(60,y,'Operator',44,'SemiBold');d.text(625,y,'Server',44,'SemiBold');y+=90
        d.line((left,y),(left,y+1150),dashed=True)
        d.line((right,y),(right,y+1150),dashed=True)
        d.text(160,y,'Casey assignment\nExpected version 2',46,width=610)
        d.arrow((left,y+145),(right,y+145));y+=205
        d.panel(160,y,650,345)
        d.text(190,y+25,'ONE ATOMIC COMMIT',36,'SemiBold','accent')
        d.text(190,y+90,'Record -> version 3\nOne history event\nSaved response receipt',44,width=590)
        d.arrow((right,y+390),(left+160,y+390),dashed=True)
        d.line((left+140,y+370),(left+180,y+410),role='text')
        d.line((left+140,y+410),(left+180,y+370),role='text')
        d.text(235,y+420,'Reply lost after commit',42,'SemiBold',width=610)
        y+=530
        d.text(160,y,'Explicit retry\nSame key + body',46,width=610)
        d.arrow((left,y+140),(right,y+140));y+=190
        d.text(160,y,'Current authorization\nMatching retained receipt',42,width=650)
        d.arrow((right,y+165),(left,y+165));y+=205
        d.text(140,y,'Return historical response\nRetry adds zero events',46,'SemiBold',width=700);y=d.bottom+60
        d.text(60,y,'Later resolution: version 4, four events.',42,width=840)
    else:
        left,right=230,1500
        d.text(60,y,'Operator',46,'SemiBold');d.text(1300,y,'Server transaction',46,'SemiBold',width=450);y+=90
        d.line((left,y),(left,y+820),dashed=True,z=0)
        d.line((right,y),(right,y+820),dashed=True,z=0)
        d.text(410,y,'Assign Casey; expect version 2',44,width=970)
        d.arrow((left,y+95),(right,y+95))
        d.panel(790,y+155,930,230)
        d.text(820,y+180,'ONE ATOMIC COMMIT',34,'SemiBold','accent')
        d.text(820,y+245,'Record v3 + history event + saved receipt',42,width=860)
        d.arrow((right,y+435),(left+160,y+435),dashed=True)
        d.line((left+140,y+415),(left+180,y+455),role='text')
        d.line((left+140,y+455),(left+180,y+415),role='text')
        d.text(460,y+465,'Reply lost after commit',44,'SemiBold')
        d.text(420,y+560,'Retry: original key + body',44)
        d.arrow((left,y+640),(right,y+640))
        d.text(600,y+695,'Authorized receipt replay; no new event',42,width=1080)
        d.arrow((right,y+790),(left,y+790))
        d.text(60,y+850,'Historical v3 response is separate from the later current v4 state.',42,width=d.w-120)


def themes(d):
    y=d.top
    d.text(60,y,'Chrome adapter: role names become host fields',44,'SemiBold',width=d.w-120);y=d.bottom+60
    pairs=[('canvas','frame'),('panel','toolbar'),('text','tab_text')]
    for i,(role,field) in enumerate(pairs):
        yy=y+i*155
        if d.narrow:
            d.panel(60,yy,330,110);d.text(85,yy+30,role,48,'SemiBold')
            d.arrow((410,yy+55),(540,yy+55))
            d.panel(560,yy,340,110);d.text(585,yy+30,field,48,'SemiBold')
        else:
            xx=60+i*580
            d.panel(xx,yy-i*155,480,120);d.text(xx+30,y+32,role,48,'SemiBold')
            d.arrow((xx+240,y+135),(xx+240,y+230))
            d.panel(xx,y+245,480,120);d.text(xx+30,y+278,field,48,'SemiBold')
    y+=520 if d.narrow else 440
    if d.narrow:
        d.text(60,y,'One source vocabulary; host-specific adapters.',44,width=840);y=d.bottom+50
        d.text(60,y,'Package: inspect the generated manifest',44,'SemiBold',width=840)
        y=d.bottom+40
        d.text(60,y,'Browser: select a package independently of page appearance',44,width=840)
        y=d.bottom+50
        d.line((60,y),(900,y),dashed=True)
        d.text(60,y+35,'Native: separate installation and restart checks',44,'SemiBold',width=840)

    else:
        d.text(60,y,'One source vocabulary; host-specific adapters.',44);y+=100
        d.box(60,y,500,'Package + manifest','Inspectable output',h=250,size=40)
        d.box(650,y,500,'Browser preview','Independent package choice',h=250,size=40)
        d.box(1240,y,500,'Native acceptance','Separate host checks',h=250,size=40,dashed=True)
    d.text(60,max(d.bottom,max(s[3] for s in d.shapes))+45,
           'Mapping illustration. Current preview and retained downloads keep separate palette histories.',
           36,role='muted',width=d.w-120)


def calendar(d):
    y=d.top
    d.text(60,y,'Lab review  |  2026-11-01 09:00',46,'SemiBold',width=d.w-120);y=d.bottom+60
    x,w=(60,840) if d.narrow else (60,800)
    d.text(x+28,y+25,'Calendar JSON',46,'Bold')
    excerpt='{\n  "schema_version": 1,\n  "next_id": 2,\n  "events": [{"id": 1,\n    "title": "Lab review",\n    "starts_at":\n      "2026-11-01 09:00"}]\n}'
    excerpt_bottom=d.text(x+28,y+110,excerpt,38 if d.narrow else 36,width=w-56)
    json_height=max(500,math.ceil(excerpt_bottom-y+35))
    d.panel(x,y,w,json_height)
    csvy=y+json_height+60 if d.narrow else y
    csvx,csvw=(60,840) if d.narrow else (980,760)
    d.panel(csvx,csvy,csvw,290)
    d.text(csvx+28,csvy+25,'Separate CSV export',46,'Bold',width=csvw-56)
    widths=[90,285,csvw-405]
    labels=[('id','1'),('title','Lab review'),('starts_at','2026-11-01\n09:00')]
    xx=csvx+20
    for col,((heading,value),cw) in enumerate(zip(labels,widths)):
        d.text(xx+10,csvy+110,heading,32,'SemiBold',width=cw-15)
        d.text(xx+10,csvy+165,value,38 if d.narrow else 34,width=cw-15)
        if col:d.line((xx-7,csvy+100),(xx-7,csvy+265))
        xx+=cw
    d.line((csvx+20,csvy+150),(csvx+csvw-20,csvy+150))
    if not d.narrow:d.arrow((875,y+240),(960,y+240))
    y=max(y+json_height,csvy+290)+65
    d.text(60,y,'Persistence boundary',46,'SemiBold');y+=90
    if d.narrow:
        d.text(60,y,'Temporary file -> replace JSON\n-> adopt in-memory state',46,width=840)
        y=d.bottom+45;d.text(60,y,'A failed write keeps the prior state.',42,role='muted',width=840)
    else:
        d.text(60,y,'Temporary file -> replace JSON -> adopt in-memory state',44,width=d.w-120)
        d.text(60,y+90,'A failed write keeps the prior state. CSV refuses an existing destination.',38,role='muted',width=d.w-120)


DRAWERS={'runtime':runtime,'adaptive':adaptive,'atlas':atlas,'shipment':shipment,
         'themes':themes,'calendar':calendar}


def draw_project(root,project,roles,fonts,*,narrow):
    if project['renderer']=='reuse':
        layout='narrow' if narrow else 'wide'
        for ext in ('png','svg'):
            p=root/'assets/explainers'/f"{project['id']}-obscur-{layout}.{ext}"
            expected=project['reused_artifacts'][layout+'.'+ext]
            if hashlib.sha256(p.read_bytes()).hexdigest()!=expected['sha256']:
                raise ValueError('Supply the exact pinned reused figure: '+str(p))
        png=(root/'assets/explainers'/f"{project['id']}-obscur-{layout}.png").read_bytes()
        width,height=struct.unpack('>II',png[16:24])
        return {'width':width,'height':height,'kind':project['figure_class'],
                'composition':project['composition'],'reused_exact_bytes':True,
                'provenance':{k:v for k,v in project['reused_artifacts'].items() if k.startswith(layout+'.')}}
    d=Diagram(root,project,roles,fonts,narrow,height=2200 if narrow else 1500)
    DRAWERS[project['id']](d)
    return d.finish()
