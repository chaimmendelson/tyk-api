import typing
import strawberry

from typing import List

from tyk_api.src.services.organization import OrganizationService
from tyk_api.src.models import TykOrganizationModel, CreateOrganizationRequest, DeleteOrganizationRequest


@strawberry.type
class Organization:
    id: str
    cname: typing.Optional[str]
    cname_enabled: typing.Optional[bool]
    hybrid_enabled: typing.Optional[bool]
    owner_name: typing.Optional[str]
    owner_slug: typing.Optional[str]


@strawberry.input
class CreateOrganizationInput:
    app_name: str
    org_name: str


@strawberry.input
class DeleteOrganizationInput:
    app_name: str
    org_name: str


def _to_org_type(model: TykOrganizationModel) -> Organization:
    return Organization(
        id=model.id,
        cname=model.cname,
        cname_enabled=model.cname_enabled,
        hybrid_enabled=model.hybrid_enabled,
        owner_name=model.owner_name,
        owner_slug=model.owner_slug,
    )


@strawberry.type
class Query:
    @strawberry.field
    async def organizations_by_app(self, app_name: str) -> List[Organization]:
        repo = await OrganizationService.get_repo()
        orgs = await repo.get_organizations_by_application(app_name)
        return [_to_org_type(o) for o in orgs]


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_organization(self, input: CreateOrganizationInput) -> Organization:
        req = CreateOrganizationRequest(app_name=input.app_name, org_name=input.org_name)
        org = await OrganizationService.create_organization(req)
        return _to_org_type(org)

    @strawberry.mutation
    async def delete_organization(self, input: DeleteOrganizationInput) -> bool:
        req = DeleteOrganizationRequest(app_name=input.app_name, org_name=input.org_name)
        await OrganizationService.delete_organization(req)
        return True


schema = strawberry.Schema(query=Query, mutation=Mutation)
