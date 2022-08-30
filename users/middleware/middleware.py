from django.shortcuts import redirect


def auth_middleware(gt_response):
    def middleware(request):
        returnUrl = request.META['PATH_INFO']
        print(request.META['PATH_INFO'], "--")
        # print(request.session.get('user'))
        try:
            if not request.session['userdata'].get('email'):
                return redirect(f'/signin?returnUrl={returnUrl}')
        except:
            return redirect(f'/signin?returnUrl={returnUrl}')
        return gt_response(request)

    return middleware
