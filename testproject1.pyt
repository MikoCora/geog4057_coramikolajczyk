# -*- coding: utf-8 -*-

import arcpy
import helloworld


class Toolbox:
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "ComplexNumber"
        self.description = "Complex Number Class"

    def getParameterInfo(self):
        """Define the tool parameters."""
        param1 = arcpy.Parameter(
            displayName="Real",
            name="real",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input")
        param2 = arcpy.Parameter(
            displayName="Imaginary",
            name="imag",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input")
        param3 = arcpy.Parameter(
            displayName="Real",
            name="real",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input")
        param4 = arcpy.Parameter(
            displayName="Imaginary",
            name="imag",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input")
        params = [param1, param2, param3, param4]
        params.append(param2)
        return params

    def isLicensed(self):
        """Set whether the tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        img1 = parameters[1].value
        real1 = parameters[0].value
        img2 = parameters[3].value
        real2 = parameters[2].value
        c_1 = helloworld.ComplexNumber(real1, img1)
        c_2 = helloworld.ComplexNumber(real2, img2)
        c_3 = c_1.add(c_2)
        print(f"c_3:{c_3.real}+{c_3.imag}i")
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
