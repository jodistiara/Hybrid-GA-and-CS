class Config:
    __Popsize = 10
    __Lambda = 1.5
    __Pa = 0.2
    __Pc = 0.8
    __Pm = 0.1
    __Alpha = 0.01
    __Maxgen = 10
    __NumOfCourse = 5
    __NumOfClass = 10
    __NumOfTimeslots = 2
    # __MaxAllel = __NumOfClass * __NumOfTimeslots
    __MaxAllel = 100
    __MinAllel = 1
    __Pointer = 4

    @classmethod
    def get_popsize(self):
        return self.__Popsize

    @classmethod
    def get_Pa(self):
        return self.__Pa

    @classmethod
    def get_Pc(self):
        return self.__Pc

    @classmethod
    def get_Pm(self):
        return self.__Pm

    @classmethod
    def get_lambda(self):
        return self.__Lambda

    @classmethod
    def get_alpha(self):
        return self.__Alpha

    @classmethod
    def get_maxgen(self):
        return self.__Maxgen
    
    @classmethod
    def get_pointer(self):
        return self.__Pointer

    @classmethod
    def get_dimension(self):
        return self.__NumOfCourse

    # @classmethod
    # def set_dimension(self, _dimension):
    #     self.__NumOfCourse = _dimension

    @classmethod
    def get_maxallel(self):
        return self.__MaxAllel

    @classmethod
    def get_minallel(self):
        return self.__MinAllel
