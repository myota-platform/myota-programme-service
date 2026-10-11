from http.server import ThreadingHTTPServer

from myota_logging import configure_logging

configure_logging("myota-programmes", component="api")

from programmes import ProgrammeHandler, seed

seed()
ThreadingHTTPServer(("0.0.0.0", 8002), ProgrammeHandler).serve_forever()
