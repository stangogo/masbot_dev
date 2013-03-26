#!/usr/bin/python
# -*- coding: utf-8 -*-
  
from masbot.ui.utils import SigName, UISignals

UISignals.GetSignal(SigName.SERVO_ON).connect(self.servo_on)