from django.shortcuts import redirect


def my_view(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/auth/login/')
        return view_func(request, *args, **kwargs)
    return wrapper
