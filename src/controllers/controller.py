from itertools import product
from flask.views import MethodView
from flask import request, render_template, redirect, flash
from src.db import mysql




class IndexController(MethodView):
    def get(self):
        with mysql.cursor() as cur:
            cur.execute("SELECT * FROM produtos")
            data = cur.fetchall()
            cur.execute("SELECT * FROM categories")
            categories = cur.fetchall()
            
            return render_template('public/index.html', data=data , categories=categories) 

    
    def post(self):        
        code = request.form['code']
        name = request.form['name']
        stock = request.form['stock']
        value = request.form['value']
        category = request.form['category']

        with mysql.cursor() as cur:
            try:
                cur.execute("INSERT INTO produtos VALUES(%s, %s, %s, %s, %s)", (code, name, stock, value, category))
                cur.connection.commit()
                flash('Produto Cadastrado com Sucesso', 'success')
            except:
                flash('Produto não Cadastrado', 'error')
            return redirect('/')


class DeleteProdutoController(MethodView):
    def post(self, code):
        with mysql.cursor() as cur:
            try:
                cur.execute("DELETE FROM produtos WHERE code =%s",(code,))
                cur.connection.commit()
                flash('Produto Deletado com Sucesso', 'success')
            except:
                flash('Este Produto não foi Deletado', 'error')
            return redirect('/')


class UpdateProdutoController(MethodView):
    def get(self, code):
        with mysql.cursor() as cur:
            cur.execute("SELECT * FROM produtos WHERE code =%s",(code,))
            product = cur.fetchone()
            return render_template('public/update.html',product=product)


    def post(self, code):

        productCode = request.form['code']
        name = request.form['name']
        stock = request.form['stock']
        value = request.form['value']
        with mysql.cursor() as cur:
            try:
                cur.execute("UPDATE produtos SET code = %s, name = %s, stock = %s, value = %s WHERE code = %s", (productCode, name, stock, value, code))
                cur.connection.commit()
                flash('Produto Editado com Sucesso', 'success')
            except:
                flash('Este Produto não foi Editado', 'error')
            return redirect('/')
        
class CategoriesController(MethodView):
    def get(self):
            return render_template("public/categories.html")

    def post(self):
        id = request.form['id']
        name = request.form['name']
        description = request.form['description']
        with mysql.cursor() as cur:
            try:
                cur.execute("INSERT INTO categories VALUES (%s, %s, %s)", (id, name, description))
                cur.connection.commit()
                flash('Categoria Cadastrada com Sucesso', 'success')
            except:
                flash('Categoria não foi Cadrastrada', 'error')
            return redirect('/')
