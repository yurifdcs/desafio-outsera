"""
Ciclo real de criação, atualização e remoção.

A BrasilAPI usada no resto da suíte é só de consulta: POST, PUT e DELETE
lá são cenário negativo (o teste espera a rejeição). Para exercitar
escrita de verdade, este fluxo usa outra API, apontada por
CRUD_API_BASE_URL. O recurso é gravado, lido de volta, alterado, lido
de novo e só então apagado — o GET no meio é o que mostra que a
mudança persistiu, e não que a API só devolveu o corpo que recebeu.
"""

from contextlib import suppress
from uuid import uuid4

import pytest

from contrato import validar_contrato

pytestmark = pytest.mark.crud


def test_cria_atualiza_e_remove_um_recurso(api_crud):
    nome = f"recurso-suite-{uuid4()}"
    nome_atualizado = f"{nome}-editado"
    recurso_id = None

    try:
        criado = api_crud.post(
            "/objects",
            data={"name": nome, "data": {"quantidade": 1}},
        )
        corpo = criado.json()
        recurso_id = corpo.get("id")

        assert criado.status == 200
        assert "application/json" in criado.headers["content-type"]
        validar_contrato(corpo, "objeto.json")
        assert corpo["name"] == nome
        assert corpo["data"]["quantidade"] == 1

        consultado = api_crud.get(f"/objects/{recurso_id}")
        assert consultado.status == 200
        assert consultado.json()["name"] == nome
        assert consultado.json()["data"]["quantidade"] == 1

        atualizado = api_crud.put(
            f"/objects/{recurso_id}",
            data={"name": nome_atualizado, "data": {"quantidade": 2}},
        )
        assert atualizado.status == 200
        validar_contrato(atualizado.json(), "objeto.json")
        assert atualizado.json()["name"] == nome_atualizado
        assert atualizado.json()["data"]["quantidade"] == 2

        confirmado = api_crud.get(f"/objects/{recurso_id}")
        assert confirmado.status == 200
        assert confirmado.json()["name"] == nome_atualizado
        assert confirmado.json()["data"]["quantidade"] == 2

        removido = api_crud.delete(f"/objects/{recurso_id}")
        assert removido.status == 200
        assert recurso_id in removido.json()["message"]

        ausente = api_crud.get(f"/objects/{recurso_id}")
        assert ausente.status == 404
        assert "error" in ausente.json()
    finally:
        if recurso_id:
            with suppress(Exception):
                api_crud.delete(f"/objects/{recurso_id}")
