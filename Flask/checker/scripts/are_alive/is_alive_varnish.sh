(curl -I -s http://localhost:6081/ | awk 'NR==1{print $2}' | ( read code && [ "$code" -eq 403 ] && echo 'Success <svg width="12" height="12" style="vertical-align: middle;"><circle cx="6" cy="6" r="6" fill="green"/></svg>' || echo 'Failure <svg width="12" height="12" style="vertical-align: middle;"><circle cx="6" cy="6" r="6" fill="red"/></svg>' ) || (sleep 10 && curl -I -s http://localhost:6081/ | awk 'NR==1{print $2}' | ( read code && [ "$code" -eq 403 ] && echo 'Success <svg width="12" height="12" style="vertical-align: middle;"><circle cx="6" cy="6" r="6" fill="green"/></svg>' || echo 'Failure <svg width="12" height="12" style="vertical-align: middle;"><circle cx="6" cy="6" r="6" fill="red"/></svg>' )))