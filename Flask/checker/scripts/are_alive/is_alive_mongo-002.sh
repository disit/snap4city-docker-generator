( docker exec mongo-002 mongo localhost --eval "printjson(db.serverStatus())" | grep -q '"ok" : 1' && echo 'Success <svg width="12" height="12" style="vertical-align: middle;"><circle cx="6" cy="6" r="6" fill="green"/></svg>' || echo 'Failure <svg width="12" height="12" style="vertical-align: middle;"><circle cx="6" cy="6" r="6" fill="red"/></svg>' ) || (sleep 10 && docker exec mongo-002 mongo localhost --eval "printjson(db.serverStatus())" | grep -q '"ok" : 1' && echo 'Success <svg width="12" height="12" style="vertical-align: middle;"><circle cx="6" cy="6" r="6" fill="green"/></svg>' || echo 'Failure <svg width="12" height="12" style="vertical-align: middle;"><circle cx="6" cy="6" r="6" fill="red"/></svg>' )