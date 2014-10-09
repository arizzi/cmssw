#include "TrackingTools/AnalyticalJacobians/interface/JacobianCurvilinearToCartesian.h"
#include "TrackingTools/TrajectoryParametrization/interface/GlobalTrajectoryParameters.h"
#include "DataFormats/GeometryVector/interface/jacobians.h"

JacobianCurvilinearToCartesian::
JacobianCurvilinearToCartesian(const GlobalTrajectoryParameters& globalParameters) :
theJacobian(jacobians::jacobianCurvilinearToCartesian(globalParameters.momentum(),globalParameters.charge())) {}


