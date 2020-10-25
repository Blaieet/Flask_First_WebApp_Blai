
from flask import make_response
from flask import redirect
from flask import request, url_for,abort
from fooApp.forms import ProductForm
from flask import Flask
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from flask import Response
from flask import render_template, jsonify
import bson

app = Flask(__name__)


app.config['MONGO_DBNAME'] = 'FlaskWebApp'
app.config['MONGO_URI'] = 'mongodb+srv://dbUser:ubstyle@clusterblai.olevp.azure.mongodb.net/FlaskWebApp?retryWrites=true&w=majority'

mongo = PyMongo(app)


# @app.route('/')
# def index():
#   return redirect(url_for('products_list'))

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/products/<product_id>/delete/', methods=['DELETE'])
def product_delete(product_id):
  """Delete record using HTTP DELETE, respond with JSON."""
  result = mongo.db.products.delete_one({ "_id": ObjectId(product_id) })
  if result.deleted_count == 0:
    # Abort with Not Found, but with simple JSON response.
    response = jsonify({'status': 'Not Found'})
    response.status = 404
    return response
  return jsonify({'status': 'OK'})

if __name__ == '__main__':
    app.run()


@app.route('/string/')
def return_string():
    dump = dump_request_detail(request)
    return 'Hello, world!'

@app.route('/object/')
def return_object():
    dump = dump_request_detail(request)
    headers = {'Content-Type': 'text/plain'}
    return make_response(Response('Hello, world! \n' + dump, status=200,headers=headers))

@app.route('/tuple/<path:resource>')
def return_tuple(resource):
    dump = dump_request_detail(request)
    return 'Hello, world! \n' + dump, 200, {'Content-Type': 'text/plain'}


def dump_request_detail(request):
    request_detail = ""
    
    ## Request INFO ##
    request.endpoint: {request.endpoint}
    request.method: {request.method}
    request.view_args: {request.view_args}
    request.args: {request.args}
    request.form: {request.form}
    request.user_agent: {request.user_agent}
    request.files: {request.files}
    request.is_xhr: {request.is_xhr}

    ## request.headers ##

    "".format(request=request).strip()
    return request_detail

@app.before_request
def callme_before_every_request():
    # Demo only: the before_request hook.
    app.logger.debug(dump_request_detail(request))

@app.after_request
def callme_after_every_response(response):
    # Demo only: the after_request hook.
    app.logger.debug('# After Request #\n' + repr(response))
    return response



@app.route('/products/create/', methods=['GET', 'POST'])
def product_create():
    """Provide HTML form to create a new product."""
    form = ProductForm(request.form)
    if request.method == 'POST' and form.validate():
        mongo.db.products.insert_one(form.data)
        # Success. Send user back to full product list.
        return redirect(url_for('products_list'))
    # Either first load or validation error at this point.
    return render_template('product/edit.html', form=form)

@app.route('/products/<product_id>/')
def product_detail(product_id):
    """Provide HTML page with a given product."""
    # Query: get Product object by ID.
    product = mongo.db.products.find_one({ "_id": ObjectId(product_id) })
    if product is None:
        # Abort with Not Found.
        abort(404)
    return render_template('product/detail.html',product=product)

@app.route('/products/')
def products_list():
  """Provide HTML listing of all Products."""
  # Query: Get all Products objects, sorted by date.
  products = mongo.db.products.find()[:]
  return render_template('product/index.html',products=products)

@app.route('/products/<product_id>/edit/',methods=['GET', 'POST'])
def product_edit(product_id):
    product = mongo.db.products.find_one({ "_id": ObjectId(product_id) })
    if product is None:
        abort(404)
    form = ProductForm(request.form)
    print(product)
    if request.method == 'POST' and form.validate():

        mongo.db.products.update_one({"_id":ObjectId(product_id)},
                                     {'$set':
                                            {'name':form.name.data,'description':form.description.data,'price':form.price.data},
                                      },upsert=False)

        #Update product for the render_template
        product = mongo.db.products.find_one({"_id": ObjectId(product_id)})
        # Success. Send the user back to the detail view.
        return render_template('product/detail.html', product=product)
    return render_template('product/edit.html', form=form)

@app.errorhandler(404)
def error_not_found(error):
  return render_template('error/not_found.html'), 404

@app.errorhandler(bson.errors.InvalidId)
def error_not_found(error):
  return render_template('error/not_found.html'), 404