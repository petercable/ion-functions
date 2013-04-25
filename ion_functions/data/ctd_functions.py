#!/usr/bin/env python
"""
@package ion_functions.data.ctd_functions
@file ion_functions/data/ctd_functions.py
@author Christopher Wingard
@brief Module containing CTD related data-calculations.
"""

def ctd_sbe16plus_tempwat(t0, a0, a1, a2, a3):
    """
    Description:

        OOI Level 1 Water Temperature data product, which is calculated using
        data from the Sea-Bird Electronics conductivity, temperature and depth
        (CTD) family of instruments. This document is intended to be used by
        OOI programmers to construct appropriate processes to create the L1
        water temperature product. 

    Implemented by:

        2013-04-12: Luke Campbell. Initial Code
        2013-04-12: Christopher Wingard. Minor edits
        
    Usage:

        t = ctd_sbe16plus_tempwat(t0, a0, a1, a2, a3)

            where

        t0 = temp (temperature) [unitless] (see
            1341-00010_Data_Product_SPEC_TEMPWAT_OOI.pdf)
        
        a0 = a0 (a0 calibration coefficient) [unitless] (see
            1341-00010_Data_Product_SPEC_TEMPWAT_OOI.pdf)
        
        a1 = a1 (a1 calibration coefficient) [unitless] (see
            1341-00010_Data_Product_SPEC_TEMPWAT_OOI.pdf)
        
        a2 = a2 (a2 calibration coefficient) [unitless] (see
            1341-00010_Data_Product_SPEC_TEMPWAT_OOI.pdf)
        
        a3 = a3 (a3 calibration coefficient) [unitless] (see
            1341-00010_Data_Product_SPEC_TEMPWAT_OOI.pdf)

    Example:

        [TODO]

    References:
    
        OOI (2012). Data Product Specification for Water Temperature. Document
            Control Number 1341-00010. https://alfresco.oceanobservatories.org/
            (See: Company Home >> OOI >> Controlled >> 1000 System Level >>
            1341-00010_Data_Product_SPEC_TEMPWAT_OOI.pdf)
    """
    import numpy as np

    mv = (t0 - 524288) / 1.6e7
    r = (mv * 2.9e9 + 1.024e8)/(2.048e4 - mv * 2.0e5)
    t = 1 / (a0 + a1 * np.log(r) + a2 * np.power(np.log(r),2)
           + a3 * np.power(np.log(r),3)) - 273.15
    return t


def ctd_sbe16plus_preswat(p0, therm0, ptempa0, ptempa1, ptempa2,
                          ptca0, ptca1, ptca2, ptcb0, ptcb1, ptcb2,
                          pa0, pa1, pa2):
    """
    Description:

        OOI Level 1 Pressure (Depth) data product, which is calculated using
        data from the Sea-Bird Electronics conductivity, temperature and depth
        (CTD) family of instruments. This document is intended to be used by
        OOI programmers to construct appropriate processes to create the L1
        water temperature product. 

    Implemented by:

        2013-04-12: Chris Wingard. Initial Code

    Usage:

        p = ctd_sbe16plus_preswat(p0, therm0, ptempa0, ptempa1, ptempa2,
                          ptca0, ptca1, ptca2, ptcb0, ptcb1, ptcb2,
                          pa0, pa1, pa2)

            where

        [TODO]
        
    Example:

        [TODO]

    References:
    
        OOI (2012). Data Product Specification for Pressure (Depth). Document
            Control Number 1341-00020. https://alfresco.oceanobservatories.org/
            (See: Company Home >> OOI >> Controlled >> 1000 System Level >>
            1341-00020_Data_Product_SPEC_PRESWAT_OOI.pdf)
    """
    import numpy as np
    
    # compute calibration parameters
    tv = therm0 / 13107.0
    t = ptempa0 + ptempa1 * tv + ptempa2 * tv**2
    x = p0 - ptca0 - ptca1 * t - ptca2 * t**2
    n = x * ptcb0 / (ptcb0 + ptcb1 * t + ptcb2 * t**2)
    
    # compute pressure in psi, rescale and compute in dbar and return
    p_psi = pa0 + pa1 * n + pa2 * n**2
    p_dbar = (p_psi * 0.689475729) - 10.1325
    return p_dbar


def ctd_sbe16plus_condwat(c0, t1, p1, g, h, i, j, cpcor, ctcor):
    """
    Description:

        OOI Level 1 Conductivity core data product, which is calculated using
        data from the Sea-Bird Electronics conductivity, temperature and depth
        (CTD) family of instruments. This document is intended to be used by
        OOI programmers to construct appropriate processes to create the L1
        water temperature product. 

    Implemented by:

        2013-04-12: Christopher Wingard. Initial Code

    Usage:

        t = ctd_sbe16plus_condwat(c0, t1, p1, g, h, i, j, cpcor, ctcor)

            where

        [TODO]
        
    Example:

        [TODO]

    References:
    
        OOI (2012). Data Product Specification for Water Temperature. Document
            Control Number 1341-00010. https://alfresco.oceanobservatories.org/
            (See: Company Home >> OOI >> Controlled >> 1000 System Level >>
            1341-00010_Data_Product_SPEC_TEMPWAT_OOI.pdf)
    """
    import numpy as np

    # convert raw conductivty measurement to frequency
    f = (c0 / 256.0) / 1000.0
    
    # calculate conductivity [S m-1]
    c = (g + h * f**2 + i * f**3 + j * f**4) / (1 + ctcor * t1 + cpcor * p1)
    return c


def ctd_pracsal(c, t, p):
    """
    Description:

        OOI Level 2 Practical Salinity core data product, which is calculated
        using the Thermodynamic Equations of Seawater - 2010 (TEOS-10) Version
        3.0, with data from the conductivity, temperature and depth (CTD)
        family of instruments. This calculation is defined in the Data Product
        Specification for Salinty - DCN 1341-00040.

    Implemented by:

        2013-03-13: Christopher Wingard. Initial code.

    Usage:

        SP = ctd_pracsal(c, t, p)

            where

        SP = Practical Salinity (seawater salinity, PSS-78) [unitless]
        c = conductivity (seawater conductivity) [S m-1], (see
            1341-00010_Data_Product_Spec_CONDWAT) 
        t = temperature (seawater temperature) [deg_C], (see
            1341-00030_Data_Product_Spec_TEMPWAT)
        p = pressure (sea pressure) [dbar], (see
            1341-00020_Data_Product_Spec_PRESWAT)

    Example:

        c = 5.407471
        t = 28
        p = 0

        SP = ctd_pracsal(c, t, p)
        print SP
        33.4952

    References:
    
        OOI (2012). Data Product Specification for Salinty. Document Control
            Number 1341-00040. https://alfresco.oceanobservatories.org/ (See: 
            Company Home >> OOI >> Controlled >> 1000 System Level >>
            1341-00040_Data_Product_SPEC_PRACSAL_OOI.pdf)
    """
    # Import GSW libraries
    from pygsw import vectors as gsw

    # Convert L1 Conductivity from S/m to mS/cm
    C10 = c * 10
    
    # Calculate the Practical Salinity (PSS-78) [unitless]
    SP = gsw.sp_from_c(C10, t, p)
    return SP


def ctd_density(SP, t, p, lat, lon):
    """
    Description:
    
        OOI Level 2 Density core data product, which is calculated using the
        Thermodynamic Equations of Seawater - 2010 (TEOS-10) Version 3.0, with
        data from the conductivity, temperature and depth (CTD) family of
        instruments. This calculation is defined in the Data Product
        Specification for Density - DCN 1341-00050.
        
    Implemented by:
    
        2013-03-11: Christopher Mueller. Initial code.
        2013-03-13: Christopher Wingard. Added commenting and moved to
            ctd_functions

    Usage:
    
        rho = ctd_density(SP, t, p, lat, lon)
        
            where
    
        rho = Density (seawater density) [kg m^-3]
        SP = Practical Salinity (PSS-78) [unitless], (see
            1341-00040_Data_Product_Spec_PRACSAL)
        t = temperature (seawater temperature) [deg_C], (see
            1341-00020_Data_Product_Spec_TEMPWAT)
        p = pressure (sea pressure) [dbar], (see
            1341-00020_Data_Product_Spec_PRESWAT)
        lat = latitude where input data was collected [decimal degree]
        lon = longitude where input data was collected [decimal degree]
    
    Example:
        
        SP = 33.4952
        t = 28
        p = 0
        lat = 15.00
        lon = -55.00
        
        rho = ctd_density(SP, t, p, lat, lon)
        print rho
        1021.26508777
        
    References:
    
        OOI (2012). Data Product Specification for Density. Document Control
            Number 1341-00050. https://alfresco.oceanobservatories.org/ (See:
            Company Home >> OOI >> Controlled >> 1000 System Level >>
            1341-00050_Data_Product_SPEC_DENSITY_OOI.pdf)
    """
    from pygsw import vectors as gsw

    # Calculate the Absolute Salinity (SA) from the Practical Salinity (SP)
    # [g kg^-1]
    SA = gsw.sa_from_sp(SP, p, lon, lat)
    
    # Calculate the Conservative Temperature (CT) [deg_C]
    CT = gsw.ct_from_t(SA, t, p)

    # Calculate the Density (rho) [kg m^-3]
    rho = gsw.rho(SA, CT, p)
    return rho