from system.core.router import routes

routes['default_controller'] = 'Users'
routes['/logout'] = 'Users#logout'
routes['/register'] = 'Users#register'
routes['POST']['/create'] = 'Users#create'
routes['POST']['/login'] = 'Users#login'

routes['POST']['/favorite'] = 'Trucks#favorite'
routes['POST']['/review'] = 'Trucks#review'
routes['POST']['/populateReviews'] = 'Trucks#populateReviews'
routes['POST']['/getRating'] ='Trucks#getRating'
routes['GET']['/getFavs'] = 'Trucks#getFavs'
routes['GET']['/twiliotest'] = 'Trucks#index'

