( curl -I -s https://platform3.snap4.eu/iotapp/iotapp-003/ | awk 'NR==1{print $2}' | ( read code && [ "$code" -eq 200 ] && echo 'Success <svg width="12" height="12" style="vertical-align: middle;"><circle cx="6" cy="6" r="6" fill="green"/></svg>' || echo 'Failure <svg width="12" height="12" style="vertical-align: middle;"><circle cx="6" cy="6" r="6" fill="red"/></svg>' ) || (sleep 10 && curl -I -s https://platform3.snap4.eu/iotapp/iotapp-003/ | awk 'NR==1{print $2}' | ( read code && [ "$code" -eq 200 ] && echo 'Success <svg width="12" height="12" style="vertical-align: middle;"><circle cx="6" cy="6" r="6" fill="green"/></svg>' || echo 'Failure <svg width="12" height="12" style="vertical-align: middle;"><circle cx="6" cy="6" r="6" fill="red"/></svg>' ))
