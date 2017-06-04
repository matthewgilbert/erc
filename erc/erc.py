import numpy as np
import scipy.optimize

EPS = 0.001


def calc_weights(cov, **kwargs):
    """
    Calculate the weights associated with the equal risk contribution
    portfolio. Refer to "On the Properties of Equally-Weighted Risk
    Contributions Portfolios" by Maillard, Roncalli, and  Teiletche for
    definitions.

    Parameters
    ----------
    cov: numpy.ndarray
        (N, N) covariance matrix of assets, must be positive definite

    kwargs: keyword arguments
        Key word arguements to be passed into scipy.optimize.minim

    Returns
    -------
    w: numpy.ndarray
        (N,) array of asset weights
    """

    # check matrix is PD
    np.linalg.cholesky(cov)

    N = cov.shape[0]
    x0 = np.ones(N) / N

    SCALE_FACTOR = 1000

    def fun(x):
        risk_contributions = x.dot(cov) * x
        a = np.reshape(risk_contributions, (len(risk_contributions), 1))
        risk_diffs = a - a.transpose()
        sum_risk_diffs_squared = np.sum(np.square(np.ravel(risk_diffs)))
        # https://stackoverflow.com/a/36685019/1451311
        return sum_risk_diffs_squared/SCALE_FACTOR

    bounds = [(0, 1) for i in range(N)]
    constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
    res = scipy.optimize.minimize(fun, x0, method='SLSQP', bounds=bounds,
                                  constraints=constraints,
                                  options={'ftol': 1e-20, 'maxiter': 500})
    weights = res.x
    risk = weights.dot(cov).dot(weights)
    # res.fun is the sum of squared differences in risk contributions. Taking
    # the sqrt of this puts it back in units of risk and dividing through by
    # total risk makes this in units of percent contributions to risk, which
    # makes things scale agnostic when comparing
    sum_pcr_diffs = np.sqrt(res.fun) / risk
    if not res.success:
        raise RuntimeError(res)
    if sum_pcr_diffs > EPS:
        raise RuntimeError("Ratio of root sum of squared risk contribution "
                           "differences to portfolio covariance is %s, should "
                           "be within tolerance %s of 0" % (sum_pcr_diffs,
                                                            EPS))

    return weights
