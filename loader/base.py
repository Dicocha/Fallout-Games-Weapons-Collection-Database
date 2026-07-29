from abc import ABC, abstractmethod
from pandas import DataFrame

class BaseLoader(ABC):
    """Interfaz para la estrategia de carga de datos"""
    
    @abstractmethod
    def load(self, df: DataFrame, destination: str) -> None:
        """Contrato obligatorio para guardar los datos ya procesados"""
        pass