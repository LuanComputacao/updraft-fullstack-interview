from app import app
import os


def run_dev():
    """Run the application in development mode.
    Usage: run-dev
    """
    use_reloader = not os.getenv('PYCHARM_HOSTED', app.config.get('IN_MEMORY', False))

    try:
        # Disable Flask's debugger if external debugger is requested
        use_debugger = app.debug and not app.config.get('DEBUG_EXTERNAL')
    except Exception:
        use_debugger = False

    app.run(
        host=app.config.get('LISTEN_HOST', '0.0.0.0'),
        port=app.config.get('LISTEN_PORT', 3003),
        debug=app.debug,
        use_reloader=use_reloader,
        use_debugger=use_debugger)


run_dev()
