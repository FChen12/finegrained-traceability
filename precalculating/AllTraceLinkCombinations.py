"""
Use load_data_from() to load a existing precalculated file or an AllTraceLinkCombinationsBuilder to create from embeddings
"""

from abc import abstractmethod
import abc

import FileUtil
from TwoDimensionalMatrix import TwoDimensionalMatrix
from precalculating.ArtifactToElementMap import ArtifactToElementMap


class AllTraceLinkCombinations(abc.ABC):
    CSV_FILE_PATTERN = "{folder}/{filename}.csv"
    
    def __init__(self, similarity_matrix):
        self._similarity_matrix = similarity_matrix
    
    @classmethod
    def load_data_from(cls, folder, file_name_without_extension):
        return cls(TwoDimensionalMatrix.read_from_csv(cls._build_csv_file_name(folder, file_name_without_extension)))
    
    def write_data(self, folder, file_name_without_extension):
        self._similarity_matrix.write_to_csv(self.CSV_FILE_PATTERN.format(folder, file_name_without_extension))
    
    @abstractmethod
    def all_req_file_names(self):
        pass

    @abstractmethod
    def all_code_file_names(self):
        pass
    
    @abstractmethod
    def similarity_between(self, req, code):
        """
        req and code can be files or file elements (depending on sub class)
        """
        pass
    
    @classmethod
    def _build_csv_file_name(cls, folder, file_name_without_extension):
        return cls.CSV_FILE_PATTERN.format(folder=str(folder), filename=file_name_without_extension)
    
    
class AllFileLevelTraceLinkCombinations(AllTraceLinkCombinations):
    """
        Don't use the constructor to instantiate
        
        Rows = req file names; columns = code file names; entry = similarity
        """
    
    def all_req_file_names(self):
        return self._similarity_matrix.get_row_names()

    def all_code_file_names(self):
        return self._similarity_matrix.get_column_names()
    
    def similarity_between(self, req_file_name, code_file_name):
        return self._similarity_matrix.get_value(req_file_name, code_file_name)


class TraceLinkProvider(AllTraceLinkCombinations):
    """
    Facade for an artifact to element map with the mappings between and a twoDimensionalMatrix containing
    """
    ARTIFACT_TO_ELEMENT_MAP_FILE_PATTERN = "{folder}/{filename}_a2eMap.json"
    
    def __init__(self, similarity_matrix, artifact_to_element_map):
        super(TraceLinkProvider, self).__init__(similarity_matrix)
        self._artifact_to_element_map = artifact_to_element_map
    
    @classmethod
    def load_data_from(cls, folder, file_name_without_extension):
        similarity_matrix = TwoDimensionalMatrix.read_from_csv(cls._build_csv_file_name(folder, file_name_without_extension))
        artifact_to_element_map = ArtifactToElementMap.load_from(cls.ARTIFACT_TO_ELEMENT_MAP_FILE_PATTERN.format(folder, file_name_without_extension))
        return cls(similarity_matrix, artifact_to_element_map)
    
    def write_data(self, folder, file_name_without_extension):
        super(TraceLinkProvider, self).write_data(folder, file_name_without_extension)
        self._artifact_to_element_map.write_to(self.ARTIFACT_TO_ELEMENT_MAP_FILE_PATTERN.format(folder, file_name_without_extension))
    
    def all_req_file_names(self) -> [str]:
        return self._artifact_to_element_map.all_req_file_names()

    def all_code_file_names(self) -> [str]:
        return self._artifact_to_element_map.all_code_file_names()
    
    def methods_of(self, code_file_name) -> [str]:
        return self._artifact_to_element_map.method_keys_of(code_file_name)
    
    def non_cg_elements_of(self, code_file_name) -> [str]:
        return self._artifact_to_element_map.non_cg_keys_of(code_file_name)
    
    def all_code_elements_of(self, code_file_name) -> [str]:
        return self.methods_of(code_file_name) + self.non_cg_elements_of(code_file_name)
    
    def req_elements_of(self, req_file_name) -> [str]:
        return self._artifact_to_element_map.req_element_ids_of(req_file_name)
    
    def all_method_keys(self):
        return self._artifact_to_element_map.all_method_keys()
    
    def all_non_cg_element_keys(self):
        return self._artifact_to_element_map.all_non_cg_element_keys()
    
    def similarity_between(self, req_element, code_element) -> float:
        return self._similarity_matrix.get_value(req_element, code_element)
    
    def set_matrix(self, new_matrix: TwoDimensionalMatrix):
        self._similarity_matrix = new_matrix