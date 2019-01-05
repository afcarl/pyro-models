# model file: ../example-models/ARM/Ch.12/radon_no_pool.stan
import torch
import pyro
import pyro.distributions as dist

def init_vector(name, dims=None):
    return pyro.sample(name, dist.Normal(torch.zeros(dims), 0.2 * torch.ones(dims)))



def validate_data_def(data):
    assert 'N' in data, 'variable not found in data: key=N'
    assert 'J' in data, 'variable not found in data: key=J'
    assert 'county' in data, 'variable not found in data: key=county'
    assert 'x' in data, 'variable not found in data: key=x'
    assert 'y' in data, 'variable not found in data: key=y'
    # initialize data
    N = data["N"]
    J = data["J"]
    county = data["county"]
    x = data["x"]
    y = data["y"]

def init_params(data, params):
    # initialize data
    N = data["N"]
    J = data["J"]
    county = data["county"]
    x = data["x"]
    y = data["y"]
    # assign init values for parameters
    params["a"] = init_vector("a", dims=(J)) # vector
    params["beta"] = pyro.sample("beta"))
    params["sigma_a"] = pyro.sample("sigma_a", dist.Uniform(0))
    params["sigma_y"] = pyro.sample("sigma_y", dist.Uniform(0))
    params["mu_a"] = pyro.sample("mu_a"))

def model(data, params):
    # initialize data
    N = data["N"]
    J = data["J"]
    county = data["county"]
    x = data["x"]
    y = data["y"]
    
    # init parameters
    a = params["a"]
    beta = params["beta"]
    sigma_a = params["sigma_a"]
    sigma_y = params["sigma_y"]
    mu_a = params["mu_a"]
    # initialize transformed parameters
    # model block
    # {
    y_hat = init_vector("y_hat", dims=(N)) # vector

    for i in range(1, to_int(N) + 1):
        y_hat[i - 1] = _pyro_assign(y_hat[i - 1], ((beta * _index_select(x, i - 1) ) + _index_select(a, county[i - 1] - 1) ))
    beta =  _pyro_sample(beta, "beta", "normal", [0., 1])
    mu_a =  _pyro_sample(mu_a, "mu_a", "normal", [0., 1])
    sigma_a =  _pyro_sample(sigma_a, "sigma_a", "cauchy", [0., 2.5])
    sigma_y =  _pyro_sample(sigma_y, "sigma_y", "cauchy", [0., 2.5])
    a =  _pyro_sample(a, "a", "normal", [mu_a, sigma_a])
    y =  _pyro_sample(y, "y", "normal", [y_hat, sigma_y], obs=y)
    # }

