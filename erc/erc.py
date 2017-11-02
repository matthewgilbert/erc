import numpy as np
import scipy.optimize

MAX_ALLOWED_PCR_DIFF = 0.001


def calc_weights(cov, x0=None, options=None, scale_factor=10000):
    """
    Calculate the weights associated with the equal risk contribution
    portfolio. Refer to "On the Properties of Equally-Weighted Risk
    Contributions Portfolios" by Maillard, Roncalli, and  Teiletche for
    definitions.

    Parameters
    ----------
    cov: numpy.ndarray
        (N, N) covariance matrix of assets, must be positive definite
    x0: numpy.ndarray
        (N,) initial solution guess. If None is given uses inverse of standard
        deviation regularized to be between 0 and 1.
    options: dictionary
        A dictionary of solver options. See scipy.optimize.minimize.
    scale_factor: float
        Number to scale the optimization function by, can be helpful for
        convergence

    Returns
    -------
    w: numpy.ndarray
        (N,) array of asset weights
    """

    # check matrix is PD
    np.linalg.cholesky(cov)

    if not options:
        options = {'ftol': 1e-20, 'maxiter': 800}

    def fun(x):
        # these are non normalized risk contributions, i.e. not regularized
        # by total risk, seems to help numerically
        risk_contributions = x.dot(cov) * x
        a = np.reshape(risk_contributions, (len(risk_contributions), 1))
        # broadcasts so you get pairwise differences in risk contributions
        risk_diffs = a - a.transpose()
        sum_risk_diffs_squared = np.sum(np.square(np.ravel(risk_diffs)))
        # https://stackoverflow.com/a/36685019/1451311
        return sum_risk_diffs_squared / scale_factor

    N = cov.shape[0]
    if x0 is None:
        x0 = 1 / np.sqrt(np.diag(cov))
        x0 = x0 / x0.sum()

    bounds = [(0, 1) for i in range(N)]
    constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
    res = scipy.optimize.minimize(fun, x0, method='SLSQP', bounds=bounds,
                                  constraints=constraints,
                                  options=options)
    weights = res.x
    risk_squared = weights.dot(cov).dot(weights)
    pcrs = weights.dot(cov) * weights / risk_squared
    pcrs = np.reshape(pcrs, (len(pcrs), 1))
    pcr_max_diff = np.max(np.abs(pcrs - pcrs.transpose()))
    if not res.success:
        raise RuntimeError(res)
    if pcr_max_diff > MAX_ALLOWED_PCR_DIFF:
        raise RuntimeError("Max difference in percentage contribution to risk "
                           "in decimals is %s which exceeds tolerance of %s." %
                           (pcr_max_diff, MAX_ALLOWED_PCR_DIFF))

    return weights
