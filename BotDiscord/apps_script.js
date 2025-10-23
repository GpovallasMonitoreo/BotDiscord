function doPost(e) {
  const hoja = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("incidentes_appsheet");
  const data = JSON.parse(e.postData.contents);

  hoja.appendRow([
    new Date(),                          // Fecha creación
    data.unidad,                         // Unidad de negocio
    data.departamento,                   // Departamento reporta
    data.usuario,                        // Usuario que toma la incidencia
    data.categoria,                      // Categoría principal
    data.canal,                          // Canal de reporte
    data.testigo_incidencia,             // Link imagen 1
    data.testigo_solucion,               // Link imagen 2
    data.detalles_equipo,                // Link imagen 3
    data.puntaje_riesgo,                 // Link imagen 4
    data.descripcion || "",              // Campos de texto obligatorios
    data.notas || "",
    data.estatus || "Abierto"
  ]);

  return ContentService.createTextOutput(
    JSON.stringify({ status: "ok" })
  ).setMimeType(ContentService.MimeType.JSON);
}
