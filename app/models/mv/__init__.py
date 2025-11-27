# package exports for app.models.mv
# ensure the symbol timeseries_mv is importable from app.models.mv
try:
    # if the model is implemented in a submodule timeseries_mv.py
    from .timeseries_mv import timeseries_mv
except Exception:
    # fallback: try importing from a module file named mv.py
    try:
        from .mv import timeseries_mv
    except Exception:
        # leave a clear ImportError if neither is present
        raise
__all__ = ["timeseries_mv"]
