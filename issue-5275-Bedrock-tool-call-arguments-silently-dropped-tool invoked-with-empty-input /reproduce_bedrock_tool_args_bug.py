from typing import Type
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field, ValidationError


class CityInput(BaseModel):
    city: str = Field(..., description="City name")

class TravelDetailsTool(BaseTool):
    name: str = "get_travel_details"
    description: str = "Get travel details for a city."
    args_schema: Type[BaseModel] = CityInput
    def _run(self, city: str) -> str:
        return f"Details for {city}"

def format_validation_error(tool_name: str, error: ValidationError) -> str:
    details = error.errors()[0]
    return (
        f"Tool '{tool_name}' arguments validation failed: 1 validation error for CityInput\n"
        f"city\n"
        f"{details['msg']} [type={details['type']}, input_value={details['input']}, input_type=dict]"
    )


if __name__ == "__main__":
    print("Error in 1.9.3:")
    try:
        TravelDetailsTool()._run()
    except TypeError as exc:
        print(exc)

    print()
    print("Error in 1.13.0:")
    try:
        CityInput.model_validate({})
    except ValidationError as exc:
        print(format_validation_error("get_travel_details", exc))

    assert str(TravelDetailsTool()._run)  # keep the tool class referenced