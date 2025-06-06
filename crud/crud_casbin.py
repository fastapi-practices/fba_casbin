#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from uuid import UUID

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.plugin.casbin_rbac.model import CasbinRule
from backend.plugin.casbin_rbac.schema.casbin_rule import DeleteAllPoliciesParam


class CRUDCasbin(CRUDPlus[CasbinRule]):
    """Casbin 规则数据库操作类"""

    async def get_list(self, ptype: str, sub: str) -> Select:
        """
        获取策略列表

        :param ptype: 策略类型
        :param sub: 用户 UUID / 角色 ID
        :return:
        """
        return await self.select_order('id', 'desc', ptype=ptype, v0__like=f'%{sub}%')

    async def delete_policies_by_sub(self, db: AsyncSession, sub: DeleteAllPoliciesParam) -> int:
        """
        删除角色所有 P 策略

        :param db: 数据库会话
        :param sub: 删除所有 P 策略参数
        :return:
        """
        filters = [sub.role]
        if sub.uuid:
            filters.append(sub.uuid)

        return await self.delete_model_by_column(db, allow_multiple=True, v0__mor={'eq': filters})

    async def delete_groups_by_uuid(self, db: AsyncSession, uuid: UUID) -> int:
        """
        删除用户所有 G 策略

        :param db: 数据库会话
        :param uuid: 用户 UUID
        :return:
        """
        return await self.delete_model_by_column(db, allow_multiple=True, v0=str(uuid))


casbin_dao: CRUDCasbin = CRUDCasbin(CasbinRule)
