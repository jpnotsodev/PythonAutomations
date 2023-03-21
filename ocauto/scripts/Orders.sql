WITH SAPSalesOrders AS (
	SELECT 
		MANDT,
		VBELN,
		BSTNK
	FROM
		prd.VBAK
	WHERE
		MANDT = '888'
), SAPOutboundDelivery AS (
	SELECT 
		prd.LIKP.MANDT,
		prd.LIPS.MATNR,
		prd.LIPS.VGBEL -- Reference to prd.VBAK.VBELN
	FROM
		prd.LIKP,
		prd.LIPS
	WHERE
		prd.LIKP.VBELN = prd.LIPS.VBELN
		AND prd.LIKP.MANDT = '888'
)

SELECT
	CAST(oms_header.KUNNR AS INT) AS [Customer No],
	cust.NAME1 + cust.NAME2 AS [Customer Name],
	oms_header.ORDNUM AS [Order No],
	CAST(oms_header.ERDAT AS DATE) AS [Order Date],
	CAST(oms_detail.MATNR AS BIGINT) AS [Material No],
	CAST(oms_detail.QTYORDERED AS INT) AS [Qty],
	CONVERT(DECIMAL(10, 2), oms_detail.KBETR) AS [SRP (UP)],
	CAST(oms_detail.DISCPER AS INT) AS [Discount],
	CAST(SUM ((oms_detail.QTYORDERED * oms_detail.KBETR) - 
		(oms_detail.QTYORDERED * oms_detail.KBETR) * DISCPER / 100) AS DECIMAL(10, 2)) AS [Net Amount],
	CASE WHEN oms_header.SOTYPE = 'ZOR' THEN 'Regular Order'
		WHEN oms_header.SOTYPE = 'ZKB' THEN 'Consignment Order'
		WHEN oms_header.SOTYPE = 'ZKA' THEN 'Consignment Pullout'
		WHEN oms_header.SOTYPE = 'ZKE' THEN 'Consignment Soldout'
		WHEN oms_header.SOTYPE = 'ZKB1' THEN 'Library Order'
		WHEN oms_header.SOTYPE = 'ZKA1' THEN 'Library Pullout'
		WHEN oms_header.SOTYPE = 'ZKE1' THEN 'Library Soldout'
		WHEN oms_header.SOTYPE = 'ZCL' THEN 'CE Logic Order'
		WHEN oms_header.SOTYPE = 'ZKB2' THEN 'SP Order'
		WHEN oms_header.SOTYPE = 'ZKA2' THEN 'SP Pullout'
		WHEN oms_header.SOTYPE = 'ZKE2' THEN 'SP Soldout' END AS [Trans Type],
	ISNULL(periods.periodTitle, '') AS [School Opening],
	ISNULL((SELECT 
		TOP 1 school_year 
	FROM
		ACCPAC.REY.prd.CRMPROJECTION
	WHERE
		batchid = ssy.BATCHID), '') AS [School Year],
	CAST(oms_header.PERNR AS INT) AS [AE Code]
FROM
	prd.ZSD_OMSH oms_header
		JOIN
			prd.ZSD_OMSD oms_detail
		ON
			oms_header.ORDNUM = oms_detail.ORDNUM
			AND oms_header.MANDT = oms_detail.MANDT
		LEFT JOIN
			prd.KNA1 cust
		ON
			oms_header.KUNNR = cust.KUNNR
			AND oms_header.MANDT = cust.MANDT
		LEFT JOIN
			prd.ZSD_OMS_SSY ssy
		ON
			ssy.ORDNUM = oms_header.ORDNUM
		LEFT JOIN
			ACCPAC.REY.prd.CRMDATEPERIODS periods
		ON
			periods.periodID = ssy.SCHOOLOPENING
		JOIN
			(SELECT
				SAPSalesOrders.MANDT,
				SAPSalesOrders.BSTNK,
				SAPOutboundDelivery.MATNR
			FROM
				SAPSalesOrders,
				SAPOutboundDelivery
			WHERE
				SAPSalesOrders.VBELN = SAPOutboundDelivery.VGBEL
				AND SAPSalesOrders.MANDT = SAPOutboundDelivery.MANDT
				AND SAPSalesOrders.MANDT = '888') outbound
		ON
			outbound.BSTNK = oms_header.ORDNUM
			AND outbound.MANDT = oms_header.MANDT
			AND outbound.MATNR = oms_detail.MATNR
WHERE
	oms_header.MANDT = '888'
	AND LEFT(oms_header.ERDAT, 6) = ?
	AND
		oms_header.SOTYPE IN ('ZOR', 'ZKB')
GROUP BY
	oms_header.KUNNR,
	cust.NAME1 + cust.NAME2,
	oms_header.ORDNUM,
	CAST(oms_header.ERDAT AS DATE),
	oms_detail.MATNR,
	oms_detail.QTYORDERED,
	oms_detail.KBETR,
	oms_detail.DISCPER,
	oms_header.SOTYPE,
	periods.periodTitle,
	ssy.BATCHID,
	CAST(oms_header.PERNR AS INT)