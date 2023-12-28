import requests
import json
from typing import List, Dict, Any, Optional


class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_home(self) -> Dict[str, Any]:
        url = f"{self.base_url}/"
        response = requests.get(url)
        return response.json()

    def text_to_image(
        self, text2img_request: Dict[str, Any], accept: str = "application/json"
    ) -> Any:
        url = f"{self.base_url}/v1/generation/text-to-image"
        headers = {"Accept": accept}
        response = requests.post(url, headers=headers, json=text2img_request)
        return response.content if accept == "image/png" else response.json()

    def img_upscale_or_vary(
        self,
        data: Dict[str, Any],
        files: Dict[str, Any],
        accept: str = "application/json",
    ) -> Any:
        url = f"{self.base_url}/v1/generation/image-upscale-vary"
        headers = {"Accept": accept}
        response = requests.post(url, headers=headers, files=files, data=data)
        return response.content if accept == "image/png" else response.json()

    def img_upscale_or_vary_v2(
        self,
        img_upscale_or_vary_request: Dict[str, Any],
        accept: str = "application/json",
    ) -> Any:
        url = f"{self.base_url}/v2/generation/image-upscale-vary"
        headers = {"Accept": accept}
        response = requests.post(url, headers=headers, json=img_upscale_or_vary_request)
        return response.content if accept == "image/png" else response.json()

    def img_inpaint_or_outpaint(
        self,
        data: Dict[str, Any],
        files: Dict[str, Any],
        accept: str = "application/json",
    ) -> Any:
        url = f"{self.base_url}/v1/generation/image-inpait-outpaint"
        headers = {"Accept": accept}
        response = requests.post(url, headers=headers, files=files, data=data)
        return response.content if accept == "image/png" else response.json()

    def img_inpaint_or_outpaint_v2(
        self,
        img_inpaint_or_outpaint_request: Dict[str, Any],
        accept: str = "application/json",
    ) -> Any:
        url = f"{self.base_url}/v2/generation/image-inpait-outpaint"
        headers = {"Accept": accept}
        response = requests.post(
            url, headers=headers, json=img_inpaint_or_outpaint_request
        )
        return response.content if accept == "image/png" else response.json()

    def img_prompt(
        self,
        data: Dict[str, Any],
        files: Dict[str, Any],
        accept: str = "application/json",
    ) -> Any:
        url = f"{self.base_url}/v1/generation/image-prompt"
        headers = {"Accept": accept}
        response = requests.post(url, headers=headers, files=files, data=data)
        return response.content if accept == "image/png" else response.json()

    def img_prompt_v2(
        self, img_prompt_request: Dict[str, Any], accept: str = "application/json"
    ) -> Any:
        url = f"{self.base_url}/v2/generation/image-prompt"
        headers = {"Accept": accept}
        response = requests.post(url, headers=headers, json=img_prompt_request)
        return response.content if accept == "image/png" else response.json()

    def query_job(
        self, job_id: int, require_step_preview: Optional[bool] = False
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/v1/generation/query-job"
        params = {"job_id": job_id, "require_step_preivew": require_step_preview}
        response = requests.get(url, params=params)
        return response.json()

    def job_queue(self) -> Dict[str, Any]:
        url = f"{self.base_url}/v1/generation/job-queue"
        response = requests.get(url)
        return response.json()

    def stop(self) -> Dict[str, Any]:
        url = f"{self.base_url}/v1/generation/stop"
        response = requests.post(url)
        return response.json()

    def all_models(self) -> Dict[str, Any]:
        url = f"{self.base_url}/v1/engines/all-models"
        response = requests.get(url)
        return response.json()

    def refresh_models(self) -> Dict[str, Any]:
        url = f"{self.base_url}/v1/engines/refresh-models"
        response = requests.post(url)
        return response.json()

    def all_styles(self) -> List[str]:
        url = f"{self.base_url}/v1/engines/styles"
        response = requests.get(url)
        return response.json()
