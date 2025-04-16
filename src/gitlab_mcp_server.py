import os
from typing import List, Optional
from fastmcp import FastMCP
from pydantic import BaseModel
import gitlab
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("GitLab MCP Server")

# Initialize GitLab client
def get_gitlab_client():
    url = os.getenv("GITLAB_URL", "https://gitlab.com")
    token = os.getenv("GITLAB_TOKEN")
    if not token:
        raise ValueError("GITLAB_TOKEN environment variable is not set")
    return gitlab.Gitlab(url=url, private_token=token)

# Models for request/response
class FileContent(BaseModel):
    file_path: str
    content: str

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    visibility: str = "private"
    initialize_with_readme: bool = True

class MergeRequestCreate(BaseModel):
    title: str
    source_branch: str
    target_branch: str
    description: Optional[str] = None
    draft: bool = False

class LineComment(BaseModel):
    line: int
    content: str
    path: str
    position_type: str = "text"

# GitLab tools
@mcp.tool()
def search_repositories(search: str, page: int = 1, per_page: int = 20) -> dict:
    """Search for GitLab projects"""
    gl = get_gitlab_client()
    projects = gl.projects.list(search=search, page=page, per_page=per_page)
    return {"projects": [{"id": p.id, "name": p.name, "path": p.path_with_namespace} for p in projects]}

@mcp.tool()
def create_repository(name: str, description: Optional[str] = None, visibility: str = "private", initialize_with_readme: bool = True) -> dict:
    """Create a new GitLab project"""
    gl = get_gitlab_client()
    project = gl.projects.create({
        'name': name,
        'description': description,
        'visibility': visibility,
        'initialize_with_readme': initialize_with_readme
    })
    return {"id": project.id, "name": project.name, "web_url": project.web_url}

@mcp.tool()
def get_file_contents(project_id: str, file_path: str, ref: Optional[str] = None) -> dict:
    """Get the contents of a file from a GitLab project"""
    gl = get_gitlab_client()
    project = gl.projects.get(project_id)
    try:
        f = project.files.get(file_path=file_path, ref=ref or project.default_branch)
        return {"content": f.decode().decode()}
    except gitlab.exceptions.GitlabGetError:
        return {"error": f"File {file_path} not found"}

@mcp.tool()
def create_or_update_file(project_id: str, file_path: str, content: str, commit_message: str, branch: str) -> dict:
    """Create or update a file in a GitLab project"""
    gl = get_gitlab_client()
    project = gl.projects.get(project_id)
    try:
        # Try to update existing file
        f = project.files.get(file_path=file_path, ref=branch)
        f.content = content
        f.save(branch=branch, commit_message=commit_message)
    except gitlab.exceptions.GitlabGetError:
        # Create new file
        project.files.create({
            'file_path': file_path,
            'branch': branch,
            'content': content,
            'commit_message': commit_message
        })
    return {"status": "success", "file_path": file_path}

@mcp.tool()
def create_merge_request(project_id: str, title: str, source_branch: str, target_branch: str, 
                        description: Optional[str] = None, draft: bool = False) -> dict:
    """Create a new merge request in a GitLab project"""
    gl = get_gitlab_client()
    project = gl.projects.get(project_id)
    payload = {
        'title': title,
        'source_branch': source_branch,
        'target_branch': target_branch,
        'draft': draft
    }
    if description is not None:
        payload['description'] = description
    mr = project.mergerequests.create(payload)
    return {
        "id": mr.iid,
        "web_url": mr.web_url,
        "state": mr.state
    }

@mcp.tool()
def create_issue(project_id: str, title: str, description: Optional[str] = None, 
                 labels: Optional[List[str]] = None) -> dict:
    """Create a new issue in a GitLab project"""
    gl = get_gitlab_client()
    project = gl.projects.get(project_id)
    issue = project.issues.create({
        'title': title,
        'description': description,
        'labels': labels or []
    })
    return {
        "id": issue.iid,
        "web_url": issue.web_url,
        "state": issue.state
    }

@mcp.tool()
def create_merge_request_line_comment(
    project_id: str,
    merge_request_iid: int,
    position: dict,
    content: str
) -> dict:
    """Create a comment on a specific line in a merge request.
    
    Args:
        project_id: The ID or URL-encoded path of the project
        merge_request_iid: The internal ID of the merge request
        position: The position data for the comment, including new_path and new_line
        content: The content of the comment
    """
    gl = get_gitlab_client()
    project = gl.projects.get(project_id)
    mr = project.mergerequests.get(merge_request_iid)
    
    # Create the comment using the provided position data
    note = mr.discussions.create({
        'body': content,
        'position': position
    })
    
    return {
        "id": note.id,
        "body": content
    }

@mcp.tool()
def get_merge_request_diff(project_id: str, merge_request_iid: int) -> dict:
    """Get the diff of a merge request to find valid line positions for comments."""
    gl = get_gitlab_client()
    project = gl.projects.get(project_id)
    mr = project.mergerequests.get(merge_request_iid)
    
    # Get the diff refs
    diff_refs = mr.diff_refs
    
    # Fetch the changes
    changes = mr.changes()
    
    # Process the changes to include necessary information
    diffs = []
    for change in changes['changes']:
        diff = {
            'old_path': change['old_path'],
            'new_path': change['new_path'],
            'diff_refs': diff_refs,
            'diff': change['diff']
        }
        diffs.append(diff)
    
    return {"diffs": diffs}

if __name__ == "__main__":
    mcp.run()