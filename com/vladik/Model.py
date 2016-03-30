import numpy as np
class Model:
    def engle_granger_step_one(self):
        constant = np.ones((self.independent.shape[0], 1))
        covariates = np.concatenate((constant, self.independent), axis=1)

        theta = np.linalg.lstsq(covariates, self.dependent)[0]
        residuals = self.independent - np.dot(covariates, theta)

        return {"theta": theta, "residuals": residuals}
