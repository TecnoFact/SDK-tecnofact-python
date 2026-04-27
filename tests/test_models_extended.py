import pytest
from decimal import Decimal
from tecnofact.models import (
    Emisor,
    Receptor,
    Concepto,
    ImpuestosConcepto,
    Traslado,
    Retencion,
    TrasladoGlobal,
    RetencionGlobal,
    Impuestos,
    CfdiRelacionados,
    Cfdi4Request,
    CuentaPredial,
    InformacionAduanera,
    Parte
)


class TestImpuestosExtended:
    """Tests adicionales para mejorar cobertura de Impuestos"""
    
    def test_impuestos_empty(self):
        impuestos = Impuestos()
        
        assert impuestos.total_impuestos_trasladados is None
        assert impuestos.total_impuestos_retenidos is None
        assert impuestos.traslados is None
        assert impuestos.retenciones is None
    
    def test_impuestos_with_traslados(self):
        traslado = TrasladoGlobal(
            impuesto="002",
            tipo_factor="Tasa",
            tasa_o_cuota=Decimal("0.160000"),
            importe=Decimal("1600.00")
        )
        
        impuestos = Impuestos(
            total_impuestos_trasladados=Decimal("1600.00"),
            traslados=[traslado]
        )
        
        assert impuestos.total_impuestos_trasladados == Decimal("1600.00")
        assert len(impuestos.traslados) == 1
    
    def test_impuestos_with_retenciones(self):
        retencion = RetencionGlobal(
            impuesto="001",
            importe=Decimal("1000.00")
        )
        
        impuestos = Impuestos(
            total_impuestos_retenidos=Decimal("1000.00"),
            retenciones=[retencion]
        )
        
        assert impuestos.total_impuestos_retenidos == Decimal("1000.00")
        assert len(impuestos.retenciones) == 1
    
    def test_impuestos_to_dict_empty(self):
        impuestos = Impuestos()
        data = impuestos.to_dict()
        
        assert data == {}
    
    def test_impuestos_to_dict_complete(self):
        traslado = TrasladoGlobal(
            impuesto="002",
            tipo_factor="Tasa",
            tasa_o_cuota=Decimal("0.160000"),
            importe=Decimal("1600.00")
        )
        
        retencion = RetencionGlobal(
            impuesto="001",
            importe=Decimal("1000.00")
        )
        
        impuestos = Impuestos(
            total_impuestos_trasladados=Decimal("1600.00"),
            total_impuestos_retenidos=Decimal("1000.00"),
            traslados=[traslado],
            retenciones=[retencion]
        )
        
        data = impuestos.to_dict()
        
        assert data["total_impuestos_trasladados"] == 1600.00
        assert data["total_impuestos_retenidos"] == 1000.00
        assert len(data["traslados"]) == 1
        assert len(data["retenciones"]) == 1


class TestConceptoExtended:
    """Tests adicionales para mejorar cobertura de Concepto"""
    
    def test_concepto_with_all_optional_fields(self):
        cuenta_predial = CuentaPredial(numero="123456")
        informacion_aduanera = InformacionAduanera(
            numero_pedimento="12  34  5678  9012345"
        )
        parte = Parte(
            clave_prod_serv="01010101",
            cantidad=Decimal("1"),
            descripcion="Parte 1",
            valor_unitario=Decimal("100.00"),
            importe=Decimal("100.00")
        )
        
        concepto = Concepto(
            clave_prod_serv="01010101",
            cantidad=Decimal("1"),
            clave_unidad="E48",
            descripcion="Servicio de desarrollo",
            valor_unitario=Decimal("10000.00"),
            importe=Decimal("10000.00"),
            objeto_imp="02",
            no_identificacion="ID123",
            unidad="Servicio",
            descuento=Decimal("500.00"),
            cuenta_predial=cuenta_predial,
            informacion_aduanera=[informacion_aduanera],
            partes=[parte]
        )
        
        data = concepto.to_dict()
        
        assert data["no_identificacion"] == "ID123"
        assert data["unidad"] == "Servicio"
        assert data["descuento"] == 500.00
        assert "cuenta_predial" in data
        assert "informacion_aduanera" in data
        assert "partes" in data
        assert len(data["partes"]) == 1


class TestCfdi4RequestExtended:
    """Tests adicionales para mejorar cobertura de Cfdi4Request"""
    
    def test_cfdi4_request_with_all_optional_fields(self):
        emisor = Emisor(
            rfc="XAXX010101000",
            nombre="EMPRESA EMISORA SA DE CV",
            regimen_fiscal="601",
            cp="06300"
        )
        
        receptor = Receptor(
            rfc="XEXX010101000",
            nombre="CLIENTE SA DE CV",
            domicilio_fiscal_receptor="06400",
            regimen_fiscal_receptor="601",
            uso_cfdi="G03"
        )
        
        concepto = Concepto(
            clave_prod_serv="01010101",
            cantidad=Decimal("1"),
            clave_unidad="E48",
            descripcion="Servicio de desarrollo",
            valor_unitario=Decimal("10000.00"),
            importe=Decimal("10000.00"),
            objeto_imp="02"
        )
        
        impuestos = Impuestos(
            total_impuestos_trasladados=Decimal("1600.00")
        )
        
        cfdi_relacionados = CfdiRelacionados(
            tipo_relacion="01",
            uuids=["UUID1"]
        )
        
        cfdi = Cfdi4Request(
            emisor=emisor,
            receptor=receptor,
            conceptos=[concepto],
            tipo_comprobante="I",
            forma_pago="01",
            metodo_pago="PUE",
            moneda="MXN",
            subtotal=Decimal("10000.00"),
            total=Decimal("11600.00"),
            exportacion="01",
            serie="A",
            folio="12345",
            fecha="2024-01-15T10:00:00",
            lugar_expedicion="06300",
            tipo_cambio=Decimal("1.0"),
            descuento=Decimal("500.00"),
            impuestos=impuestos,
            cfdi_relacionados=[cfdi_relacionados],
            condiciones_pago="Pago en 30 días"
        )
        
        data = cfdi.to_dict()
        
        assert data["serie"] == "A"
        assert data["folio"] == "12345"
        assert data["fecha"] == "2024-01-15T10:00:00"
        assert data["lugar_expedicion"] == "06300"
        assert data["tipo_cambio"] == 1.0
        assert data["descuento"] == 500.00
        assert "impuestos" in data
        assert "cfdi_relacionados" in data
        assert data["condiciones_pago"] == "Pago en 30 días"


class TestReceptorExtended:
    """Tests adicionales para mejorar cobertura de Receptor"""
    
    def test_receptor_with_optional_fields(self):
        receptor = Receptor(
            rfc="XEXX010101000",
            nombre="CLIENTE SA DE CV",
            domicilio_fiscal_receptor="06400",
            regimen_fiscal_receptor="601",
            uso_cfdi="G03",
            num_reg_id_trib="123456",
            residencia_fiscal="USA"
        )
        
        data = receptor.to_dict()
        
        assert data["num_reg_id_trib"] == "123456"
        assert data["residencia_fiscal"] == "USA"


class TestInformacionAduaneraExtended:
    """Tests adicionales para mejorar cobertura de InformacionAduanera"""
    
    def test_informacion_aduanera_with_optional_fields(self):
        info = InformacionAduanera(
            numero_pedimento="12  34  5678  9012345",
            fecha="2024-01-15",
            aduana="01"
        )
        
        data = info.to_dict()
        
        assert data["numero_pedimento"] == "12  34  5678  9012345"
        assert data["fecha"] == "2024-01-15"
        assert data["aduana"] == "01"


class TestParteExtended:
    """Tests adicionales para mejorar cobertura de Parte"""
    
    def test_parte_with_optional_fields(self):
        parte = Parte(
            clave_prod_serv="01010101",
            cantidad=Decimal("1"),
            unidad="Pieza",
            descripcion="Parte 1",
            valor_unitario=Decimal("100.00"),
            importe=Decimal("100.00")
        )
        
        data = parte.to_dict()
        
        assert data["clave_prod_serv"] == "01010101"
        assert data["cantidad"] == 1.0
        assert data["unidad"] == "Pieza"
        assert data["descripcion"] == "Parte 1"
        assert data["valor_unitario"] == 100.00
        assert data["importe"] == 100.00


class TestRetencionGlobalExtended:
    """Tests adicionales para mejorar cobertura de RetencionGlobal"""
    
    def test_retencion_global_to_dict(self):
        retencion = RetencionGlobal(
            impuesto="001",
            importe=Decimal("1000.00")
        )
        
        data = retencion.to_dict()
        
        assert data["impuesto"] == "001"
        assert data["importe"] == 1000.00


class TestTrasladoGlobalExtended:
    """Tests adicionales para mejorar cobertura de TrasladoGlobal"""
    
    def test_traslado_global_to_dict(self):
        traslado = TrasladoGlobal(
            impuesto="002",
            tipo_factor="Tasa",
            tasa_o_cuota=Decimal("0.160000"),
            importe=Decimal("1600.00")
        )
        
        data = traslado.to_dict()
        
        assert data["impuesto"] == "002"
        assert data["tipo_factor"] == "Tasa"
        assert data["tasa_o_cuota"] == "0.160000"
        assert data["importe"] == 1600.00


class TestImpuestosConceptoExtended:
    """Tests adicionales para mejorar cobertura de ImpuestosConcepto"""
    
    def test_impuestos_concepto_with_retenciones(self):
        retencion = Retencion(
            base=Decimal("10000.00"),
            impuesto="001",
            tipo_factor="Tasa",
            tasa_o_cuota=Decimal("0.100000"),
            importe=Decimal("1000.00")
        )
        
        impuestos = ImpuestosConcepto(retenciones=[retencion])
        data = impuestos.to_dict()
        
        assert "retenciones" in data
        assert len(data["retenciones"]) == 1
