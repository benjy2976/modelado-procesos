"""Identificadores BPMN estables compartidos por generador y visor."""

import uuid

NS_UUID = uuid.UUID("6f1c2a7e-3b0d-4c8e-9a51-2d7f4e8b9c10")


def gid(*partes: str) -> str:
    return "_" + str(uuid.uuid5(NS_UUID, "|".join(partes)))
