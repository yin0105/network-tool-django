from django.shortcuts import render
from django.http import JsonResponse
# import whois
import subprocess
from .forms import WhoisForm


def home_view(request):
    whois_form = WhoisForm()
    context = {
        "whois_form": whois_form,
    }
    return render(request, "home.html", context)

def call_cmd(params):
    try:
        result = subprocess.check_output(params, shell=True).decode("utf-8") 
        return {"result": result}
    except Exception as e:
        return {"error_msg": "{}".format(e)}
        

def whois_ip(request):
    # if request.is_ajax():
    if request.method == 'POST':
        form = WhoisForm(request.POST)

        if form.is_valid():
            command = form.cleaned_data.get("command")
            domain_name = form.cleaned_data.get("whois_domain_name")
        # command = request.POST.get('command', None)
        # domain_name = request.POST.get('domain_name', None)
            resp_json = {}
            last_key = ""

        # if command == "whois":
            if domain_name:
                batcmd = "whois {}".format(domain_name)
                cmd_result = call_cmd(batcmd)
                
                if "error_msg" in cmd_result:
                    return JsonResponse({"error_msg": cmd_result["error_msg"]})

                for line in cmd_result["result"].splitlines():
                    if line.find(">>>") == 0: break
                    sublines = line.split(": ", 1)
                    if len(sublines) > 1:
                        if sublines[0] in resp_json:
                            resp_json[sublines[0]] += "\n" + sublines[1]
                        else:
                            resp_json[sublines[0]] = sublines[1]
                        last_key = sublines[0]
                    else:
                        if last_key != "" :
                            resp_json[last_key] += "\n" + line
            return JsonResponse(resp_json)
        
        else:
            print("=======  invalid")
            print(form.errors.as_json())
            return JsonResponse({"invalid": form.errors.as_json()})

