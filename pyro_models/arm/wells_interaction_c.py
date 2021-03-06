# model file: example-models/ARM/Ch.5/wells_interaction_c.stan
import torch
import pyro
import pyro.distributions as dist

def init_vector(name, dims=None):
    return pyro.sample(name, dist.Normal(torch.zeros(dims), 0.2 * torch.ones(dims)).to_event(1))



def validate_data_def(data):
    assert 'N' in data, 'variable not found in data: key=N'
    assert 'switched' in data, 'variable not found in data: key=switched'
    assert 'dist' in data, 'variable not found in data: key=dist'
    assert 'arsenic' in data, 'variable not found in data: key=arsenic'
    # initialize data
    N = data["N"]
    switched = data["switched"]
    dist = data["dist"]
    arsenic = data["arsenic"]

def transformed_data(data):
    # initialize data
    mean = torch.mean
    N = data["N"]
    switched = data["switched"]
    dist = data["dist"]
    arsenic = data["arsenic"]
    c_dist100 = (dist - mean(dist)) / 100.0
    c_arsenic = arsenic - mean(arsenic)
    inter     = c_dist100 * c_arsenic
    data["c_dist100"] = c_dist100
    data["c_arsenic"] = c_arsenic
    data["inter"] = inter

def init_params(data):
    params = {}
    # assign init values for parameters
    params["beta"] = init_vector("beta", dims=(4)) # vector

    return params

def model(data, params):
    # initialize data
    N = data["N"]
    switched = data["switched"]
    arsenic = data["arsenic"]
    # initialize transformed data
    c_dist100 = data["c_dist100"]
    c_arsenic = data["c_arsenic"]
    inter = data["inter"]

    # init parameters
    beta = params["beta"]
    # initialize transformed parameters
    # model block

    with pyro.plate("data", N):
        switched = pyro.sample('switched', dist.Bernoulli(logits=beta[0] + beta[1] * c_dist100 + beta[2] * c_arsenic + beta[3] * inter), obs=switched)

