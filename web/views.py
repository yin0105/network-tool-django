from django.shortcuts import render
from django.http import JsonResponse
import whois
import os
import subprocess


def home_view(request):
    return render(request, "home.html")

def whois_ip(request):
    if request.is_ajax():
        ip_addr = request.POST.get('ip_addr', None)
        if ip_addr:
            batcmd = "whois {}".format(ip_addr)
            result = subprocess.check_output(batcmd, shell=True).decode("utf-8") 
            resp_json = {}
            last_key = ""
            print("========== result ")
            print(result)
            # result = os.system("whois {}".format(ip_addr))
            for line in result.splitlines():
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

            # ip_result = whois.whois(ip_addr)
            # response = {
            #     'domain_name':ip_result.domain_name,
            #     'org':ip_result.org,
            #     'emails':ip_result.emails,
            #     'state':ip_result.state,
            #     'country':ip_result.country,
            #     'domain_name':ip_result.domain_name,
            #     'registrar':ip_result.registrar,
            #     'expiration_date':ip_result.expiration_date,
            #     'name_servers':ip_result.name_servers
            #     }
    return JsonResponse(resp_json)
