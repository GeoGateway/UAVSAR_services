
"""
	wsgi.py
		-- run as flask wrapper as wsgi application
		-- run as non-root user: ~/miniconda3/bin/mod_wsgi-express start-server wsgi.py &
"""
##################
# FOR PRODUCTION
##################

from app import create_app
application = create_app()

if __name__ == "__main__":
    ####################
    # FOR PRODUCTION
    ####################
    application.run(host='0.0.0.0', debug=False)
