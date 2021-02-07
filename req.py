import requests
import json

def get_logintoken(pagina):
    cadena_logintoken = 'name="logintoken" value="'
    posicion = pagina.find(cadena_logintoken)
    posicion += len(cadena_logintoken)
    posicion2 = pagina.find('"', posicion)
    logintoken = pagina[posicion:posicion2]
    return logintoken

def get_sesskey(pagina):
    cadena_sesskey = '"sesskey":"'
    posicion = pagina.find(cadena_sesskey)
    posicion += len(cadena_sesskey)
    posicion2 = pagina.find('"', posicion)
    sesskey = pagina[posicion:posicion2]
    return sesskey

abreviaciones = {16019:"ASO", 18968:"SRI", 15478:"IAW", 17767:"SAD", 15488:"ASGBD", 20016:"EIE"}
aules = 'https://aules.edu.gva.es/fp/login/index.php'
#usuario aules
username = ''
#password aules
password = ''

s = requests.Session()
r = s.get(aules, verify=False)
respuesta = r.text

logintoken = get_logintoken(respuesta)
credenciales = {'username':username, 'password':password, 'logintoken':logintoken}

r = s.post(aules, data=credenciales)
respuesta = r.text
sesskey = get_sesskey(respuesta)

#print("Login token: ", logintoken, "Sesskey: ", sesskey)

#print("##---##---------------------#############------------------------##---##")
#print("##---##---------------------#############------------------------##---##")
#print("##---##---------------------#############------------------------##---##")



def get_asignaturas(sesskey):
    recurso = "https://aules.edu.gva.es/fp/lib/ajax/service.php?sesskey="+sesskey+"&info=core_course_get_enrolled_courses_by_timeline_classification"
    datos = [{"index":0,"methodname":"core_course_get_enrolled_courses_by_timeline_classification","args":{"offset":0,"limit":0,"classification":"all","sort":"fullname","customfieldname":"","customfieldvalue":""}}]

    envio_json = s.post(recurso, json=datos)
    respuesta_json = envio_json.text[1:-1]
    cadena_json = json.loads(respuesta_json)
    cursos_json = cadena_json["data"]["courses"]
    cursos = {}

    for curso in cursos_json:
        nombre = curso["fullname"]
        url = curso["viewurl"]
        cursos[nombre] = url
    for k, v in cursos.items():
        print("Curso:", k, "URL:", v)

#print("##---##---------------------#############------------------------##---##")
#print("##---##---------------------#############------------------------##---##")
#print("##---##---------------------#############------------------------##---##")
def get_calendario(seskey):
    calendario = "https://aules.edu.gva.es/fp/lib/ajax/service.php?sesskey="+sesskey+"&info=core_calendar_get_calendar_monthly_view"
    fecha = [{"index":0,"methodname":"core_calendar_get_calendar_monthly_view","args":{"year":2020,"month":10,"courseid":1,"categoryid":0,"includenavigation":0,"mini":1,"day":24}}]

    envio_calendario = s.post(calendario, json=fecha)
    respuesta_calendario = envio_calendario.text[1:-1]

    cadena_calendario = json.loads(respuesta_calendario)
    calendario_json = cadena_calendario["data"]

    for semana in calendario_json["weeks"]:
        for dia in semana["days"]:
            try:
                nombre = dia["viewdaylinktitle"]
                print("----")
                print(nombre)

            except KeyError:
                pass
            for evento in dia["events"]:
                asignatura = evento["course"]["id"]
                print(evento["name"], "-", abreviaciones[asignatura])


eleccion = int(input("1 para ver las asignaturas\n2 para ver el calendario de este mes\n"))
if eleccion == 1:
    get_asignaturas(sesskey)
if eleccion == 2:
    get_calendario(sesskey)
