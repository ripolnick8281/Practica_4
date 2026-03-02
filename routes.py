from app import app, db
from flask import redirect, render_template, url_for
import formularios
from models import Tarea


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', subtitulo="Actidad en grupo TAI")


@app.route('/sobrenosotros', methods=['GET', 'POST'])
def sobrenosotros():
    formulario = formularios.FormAgregarTareas()

    if formulario.validate_on_submit():
        nueva_tarea = Tarea(titulo=formulario.titulo.data)
        db.session.add(nueva_tarea)
        db.session.commit()
        return redirect(url_for('sobrenosotros'))

    tareas = Tarea.query.order_by(Tarea.id.desc()).all()
    return render_template('sobrenosotros.html', form=formulario, tareas=tareas)

@app.route('/tareas/editar/<int:tarea_id>', methods=['GET', 'POST'])
def editar_tarea(tarea_id):
    tarea = Tarea.query.get_or_404(tarea_id)
    formulario = formularios.FormAgregarTareas()

    if formulario.validate_on_submit():
        tarea.titulo = formulario.titulo.data
        db.session.commit()
        return redirect(url_for('sobrenosotros'))

    formulario.titulo.data = tarea.titulo
    return render_template('editar_tarea.html', form=formulario, tarea=tarea)

@app.route('/tareas/eliminar/<int:tarea_id>', methods=['POST'])
def eliminar_tarea(tarea_id):
    tarea = Tarea.query.get_or_404(tarea_id)
    db.session.delete(tarea)
    db.session.commit()
    return redirect(url_for('sobrenosotros'))


@app.route('/saludo')
def saludo():
    return 'Hola bienvenido a Taller Apps '


@app.route('/usuario/<nombre>')
def usuario(nombre):
    return f'Hola {nombre} bienvenido a Taller Apps '
