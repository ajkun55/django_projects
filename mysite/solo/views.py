

from django.contrib.auth.mixins import LoginRequiredMixin
import html
from django.views import View
from django.shortcuts import render, redirect

# Create your views here.
class MainView(LoginRequiredMixin,View) :
    def get(self, request):
        msg = request.session.get('msg', False)
        if ( msg ) : del(request.session['msg'])
        return render(request, 'solo/main.html', {'message' : msg })
        # return render(request, self.template, {'message' : msg })

    def post(self, request):
        f1 = request.POST.get('field1')
        rf1 = check(f1)
        f2 = request.POST.get('field2')
        rf2 = check(f2)
        msg = rf2+' '+rf1
        request.session['msg'] = msg
        return redirect(request.path)
        # return redirect(self.success_url)



def check(s):
    msg = False
    if s :
        try:
            if not isinstance(s, str):
                raise ValueError("Input must be a string.")
            msg = s[::-1]
        except:
            msg = 'Bad format for guess:' + html.escape(s)
    return msg

