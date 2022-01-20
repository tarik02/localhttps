import functools
import asyncclick as click
from localhttps.cli.context import Context

def with_context(func):
    @click.pass_context
    @functools.wraps(func)
    def wrapper(ctx: click.core.Context, *args, **kwargs):
        ctx.obj.click = ctx
        return func(ctx.obj, *args, **kwargs)
    return wrapper
