import asyncio

def background_process(func):
    """
    Returns:
        Event loop

    Annotation to run function in background using asyncio
    """
    def wrapped(*args, **kwargs):
        """
        Returns:
            Event loop

        Wrapped function for asyncronous running of functions
        """
        return asyncio.get_event_loop().run_in_executor(None, func, *args, **kwargs)
    return wrapped