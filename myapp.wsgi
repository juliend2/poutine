import inspect
import sys
import os

def application(environ, start_response):
    status = '200 OK'
    # checker dans le python path pour voir si on a le directory actuel :
    apache_dir = os.path.dirname(os.path.realpath(inspect.getfile(inspect.currentframe())))
    project_dir = os.path.dirname(apache_dir)
    print >> environ['wsgi.errors'], str(os.path.dirname(apache_dir))
    if project_dir+'/questionlinks' not in sys.path:
        sys.path.append(project_dir+'/questionlinks') # sinon, on l'ajoute 
        
    # inclure poutine :
    import poutine as p
    poutine = p.Poutine(environ)
    dispatch_dict = poutine.dispatch()
    output = dispatch_dict['output']
    status = dispatch_dict['status']
    location = dispatch_dict['location']
    
    # ONLY FOR DEVELOPMENT!.. :
    import monitor
    monitor.start(interval=1.0)
    monitor.track(os.path.join(os.path.dirname(__file__), 'poutine.py'))
    # .../ONLY DEV!
    
    # DETECT THE MODE THAT WE'RE RUNNING IN :
    # if not environ['mod_wsgi.process_group']:
    #     output = 'EMBEDDED MODE'
    # else:
    #     output = 'DAEMON MODE'
    
    # output :
    response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(output)))]
    if status == "303 See Other" :
        response_headers.append(('Location', location))
    start_response(status, response_headers)

    return [output]
    
