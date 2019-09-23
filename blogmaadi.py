import mistune
import yaml
import os
from jinja2 import Template
from slugify import Slugify
linkify = Slugify(to_lower=True)

mdparser = mistune.Markdown()
blogfolder = '_posts/blog/'
templatefolder = 'templates/'
templates = {}
tags = set()
blogs = []

# load templates
for templatefile in os.listdir(templatefolder):
  with open(templatefolder+templatefile) as f:
    templates[templatefile[:-5]] = Template(f.read())



# load blog data
for blogfilename in os.listdir(blogfolder):
  with open(blogfolder+blogfilename) as blogfile:
    contents = blogfile.read().split('---')
    blog = yaml.load(contents[1])
    blog['date'] = blog['date'].strftime("%d %B, %Y")
    blog['html'] = mdparser(contents[2])
    blog['file'] = 'post/'+linkify(blog['title'])+'.html'
    blog['link'] = '/' + blog['file']
    blogs.append(blog)
    tags.update(blog['tags'])
    

# generate index page
with open('index.html','w') as f:
  html = templates['index'].render(blogs=blogs,tags=list(tags))
  f.write(html)
  f.close()
  print("Generated index.html")

print('')
# generate tag pages
for tag in tags:
  html = templates['tag'].render(blogs=blogs,tag=tag)
  with open('tag/'+tag+'.html','w') as f:
    f.write(html)
    f.close()
    print("Generated Tag Page: tag/" + tag + '.html')

print('')
# generate blog pages
for blog in blogs:
  html = templates['blog'].render(blog=blog)
  with open(blog['file'],'w') as f:
    f.write(html)
    f.close()
    print("Generated Blog Page: " + blog['file'] + '.html')


