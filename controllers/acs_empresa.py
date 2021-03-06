# -*- coding: utf-8 -*-
@auth.requires_login()
def index():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    if not usuario:
        redirect(URL('acs_empresa','cadastrar'))
    if usuario.tipo=="Padão":
        redirect(URL('acs_usuario','index'))
    empresa = db.empresa(usuario.empresa)
    return locals()

@auth.requires_login()
def cadastrar():
    empresa=db.empresa.insert(
        nome=auth.user.first_name+" Empresarial",)
    db.usuario_empresa.insert(empresa=empresa,usuario=auth.user.id, nome=empresa.nome)
    return redirect(URL('index'))

@auth.requires_login()
def alterar():
    response.view = 'generic.html' # view generica
    request.function='Alterar' #redefine nome da função
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    form = SQLFORM(db.empresa, usuario.empresa, deletable=False)
    if form.process().accepted:
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    return dict(form=form)


def alterar_usuario():
    response.view = 'generic.html' # view generica
    if auth.user.id!=1:
        redirect(URL('index'))
    request.function='Alterar nome da Empresa' #redefine nome da função
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    db.usuario_empresa.empresa.writable=True
    db.usuario_empresa.empresa.readable=True
    form = SQLFORM(db.usuario_empresa, usuario.id, deletable=False)
    if form.process().accepted:
#         session.flash = 'Projeto atualizado'
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    return dict(form=form)
