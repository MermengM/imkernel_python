from dataclasses import dataclass, field
from typing import Any, List, Optional, Union

from imkernel.im.method_parameter import MethodParameter


@dataclass
class MethodUnit:
    Name: str
    MethodBody: str
    Category: Optional[str] = None
    Parameter: List[MethodParameter] = field(default_factory=list)
    DataList: List[Any] = field(default_factory=list)

    def _get_call_dict(self):
        call_dict = {"fun_name": self.Name, "script_path": self.MethodBody}
        for param in self.Parameter:
            call_dict[param.ParName] = param.Value
        return call_dict

    def _generate_data_list(self):
        item = [x.Value for x in self.Parameter]
        self.DataList.append(item)

    def add_parameter(self, par: Union[MethodParameter, List[MethodParameter]]):
        if isinstance(par, list):
            self.Parameter.extend(par)
        else:
            self.Parameter.append(par)

    def to_imd(self) -> str:
        imd_content = []
        # 添加头部信息
        for data_entry in self.DataList:
            imd_content.append(f"U,{self.Name}," + ",".join(map(str, data_entry)))
        if imd_content:
            r = "\n".join(imd_content)
        else:
            r = None
        return r

    # def to_imd(self) -> str:
    #     imd_content = []
    #     # 添加头部信息
    #     for x in self.DataList:
    #         for y in x:
    #             imd_content.append(f"U,{self.Name}")

    # 添加单元信息
    # for par in self.Parameter:
    #     imd_content.append(par._to_imd())
