// LOGIN
function callMsg(category, msg) {
	if (category == 'success') {
		alertify.success(msg);
	}
	if (category == 'error') {
		alertify.error(msg);
	}
}

// MENU
function linkInventory() {
	location.href = '/inventory';
}

function linkVisits() {
	location.href = '/visits';
}

function linkGraphs() {
	location.href = '/graph';
}

function linkCards() {
	location.href = '/cards';
}

function linkRecord() {
	location.href = '/record';
}

function linkReservations() {
	location.href = '/reservations';
}

// SCRIPTS DE LAS TABLAS DE INVENTARIO
$(document).ready(function() {
	// ALL EXIT MODALS
	$('#modalAddBook').on('hidden.bs.modal', function() {
		alertify.error('Cancelado');
	});
	$('#modalAddProjector').on('hidden.bs.modal', function() {
		alertify.error('Cancelado');
	});
	$('#modalAddLibrary').on('hidden.bs.modal', function() {
		alertify.error('Cancelado');
	});
	$('#modalAddAudiovisual').on('hidden.bs.modal', function() {
		alertify.error('Cancelado');
	});
	$('#modalAddVisitor').on('hidden.bs.modal', function() {
		alertify.error('Cancelado');
	});
	$('#modalCardPregenerated').on('hidden.bs.modal', function() {
		alertify.error('Cancelado');
	});

	// OBTENCION DE IDs PARA TARJETA DE PRESTAMO DE MOBILIARIO
	var values = new Array();

	$('#tableLibrary tbody').on('click', 'tr', function() {
		$(this).toggleClass('selected');
		var value = $(this).find('td:first').html();
		var C = 0;

		for (let i = 0; i <= values.length; i++) {
			if (value != values[i]) {
				C++;
			} else {
				values.splice(i, 1);
				C--;
				break;
			}
		}

		if (C == values.length + 1) {
			values.push(value);
		}
	});

	// ENVIO DE IDs A FLASK
	$('#generar').on('click', function() {
		$.get('/getmethod/' + values);
	});

	// Tabla temporal para tarjeta de mobiliario
	var table = $('#tableTempMobiliario').DataTable({
		scrollY: 265,
		stateSave: true,
		language: {
			sProcessing: '<p class="text-primary">Procesando...',
			sLengthMenu: '<p class="text-primary">Mostrar _MENU_ registros',
			sZeroRecords: '<p class="text-primary">No se encontraron resultados',
			sEmptyTable: '<p class="text-primary">Ningún dato disponible en esta tabla',
			sInfo: '<p class="text-primary">Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros',
			sInfoEmpty: '<p class="text-primary">Mostrando registros del 0 al 0 de un total de 0 registros',
			sInfoFiltered: '<p class="text-primary">(filtrado de un total de _MAX_ registros)',
			sInfoPostFix: '<p class="text-primary">',
			sSearch: '<p class="text-primary">Buscar:',
			sUrl: '<p class="text-primary">',
			sInfoThousands: '<p class="text-primary">,',
			sLoadingRecords: '<p class="text-primary">Cargando...',
			oPaginate: {
				sFirst: '<p class="text-primary">Primero',
				sLast: '<p class="text-primary">Último',
				sNext: '<p class="text-primary">Siguiente',
				sPrevious: '<p class="text-primary">Anterior'
			},
			oAria: {
				sSortAscending: '<p class="text-primary">: Activar para ordenar la columna de manera ascendente',
				sSortDescending: '<p class="text-primary">: Activar para ordenar la columna de manera descendente'
			}
		}
	});

	// Inventario Projectors
	var table = $('#tableProjectors').DataTable({
		scrollY: 350,
		scrollX: true,
		stateSave: true,
		language: {
			sProcessing: '<p class="text-white">Procesando...',
			sLengthMenu: '<p class="text-white">Mostrar _MENU_ registros',
			sZeroRecords: '<p class="text-primary">No se encontraron resultados',
			sEmptyTable: '<p class="text-primary">Ningún dato disponible en esta tabla',
			sInfo: '<p class="text-white">Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros',
			sInfoEmpty: '<p class="text-white">Mostrando registros del 0 al 0 de un total de 0 registros',
			sInfoFiltered: '<p class="text-white">(filtrado de un total de _MAX_ registros)',
			sInfoPostFix: '<p class="text-white">',
			sSearch: '<p class="text-white">Buscar:',
			sUrl: '<p class="text-white">',
			sInfoThousands: '<p class="text-white">,',
			sLoadingRecords: '<p class="text-primary">Cargando...',
			oPaginate: {
				sFirst: '<p class="text-white">Primero',
				sLast: '<p class="text-white">Último',
				sNext: '<p class="text-white">Siguiente',
				sPrevious: '<p class="text-white">Anterior'
			},
			oAria: {
				sSortAscending: '<p class="text-white">: Activar para ordenar la columna de manera ascendente',
				sSortDescending: '<p class="text-white">: Activar para ordenar la columna de manera descendente'
			}
		}
	});

	// Inventario audiovisual
	var table = $('#tableAudiovisualRoom').DataTable({
		scrollY: 350,
		scrollX: true,
		stateSave: true,
		language: {
			sProcessing: '<p class="text-white">Procesando...',
			sLengthMenu: '<p class="text-white">Mostrar _MENU_ registros',
			sZeroRecords: '<p class="text-primary">No se encontraron resultados',
			sEmptyTable: '<p class="text-primary">Ningún dato disponible en esta tabla',
			sInfo: '<p class="text-white">Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros',
			sInfoEmpty: '<p class="text-white">Mostrando registros del 0 al 0 de un total de 0 registros',
			sInfoFiltered: '<p class="text-white">(filtrado de un total de _MAX_ registros)',
			sInfoPostFix: '<p class="text-white">',
			sSearch: '<p class="text-white">Buscar:',
			sUrl: '<p class="text-white">',
			sInfoThousands: '<p class="text-white">,',
			sLoadingRecords: '<p class="text-primary">Cargando...',
			oPaginate: {
				sFirst: '<p class="text-white">Primero',
				sLast: '<p class="text-white">Último',
				sNext: '<p class="text-white">Siguiente',
				sPrevious: '<p class="text-white">Anterior'
			},
			oAria: {
				sSortAscending: '<p class="text-white">: Activar para ordenar la columna de manera ascendente',
				sSortDescending: '<p class="text-white">: Activar para ordenar la columna de manera descendente'
			}
		}
	});

	// Inventario visits
	var table = $('#tableVisits').DataTable({
		scrollY: 350,
		scrollX: true,
		stateSave: true,
		language: {
			sProcessing: '<p class="text-white">Procesando...',
			sLengthMenu: '<p class="text-white">Mostrar _MENU_ registros',
			sZeroRecords: '<p class="text-primary">No se encontraron resultados',
			sEmptyTable: '<p class="text-primary">Ningún dato disponible en esta tabla',
			sInfo: '<p class="text-white">Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros',
			sInfoEmpty: '<p class="text-white">Mostrando registros del 0 al 0 de un total de 0 registros',
			sInfoFiltered: '<p class="text-white">(filtrado de un total de _MAX_ registros)',
			sInfoPostFix: '<p class="text-white">',
			sSearch: '<p class="text-white">Buscar:',
			sUrl: '<p class="text-white">',
			sInfoThousands: '<p class="text-white">,',
			sLoadingRecords: '<p class="text-primary">Cargando...',
			oPaginate: {
				sFirst: '<p class="text-white">Primero',
				sLast: '<p class="text-white">Último',
				sNext: '<p class="text-white">Siguiente',
				sPrevious: '<p class="text-white">Anterior'
			},
			oAria: {
				sSortAscending: '<p class="text-white">: Activar para ordenar la columna de manera ascendente',
				sSortDescending: '<p class="text-white">: Activar para ordenar la columna de manera descendente'
			}
		}
	});

	// Inventario biblioteca
	var table = $('#tableLibrary').DataTable({
		scrollY: 350,
		scrollX: true,
		stateSave: true,
		language: {
			sProcessing: '<p class="text-white">Procesando...',
			sLengthMenu: '<p class="text-white">Mostrar _MENU_ registros',
			sZeroRecords: '<p class="text-primary">No se encontraron resultados',
			sEmptyTable: '<p class="text-primary">Ningún dato disponible en esta tabla',
			sInfo: '<p class="text-white">Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros',
			sInfoEmpty: '<p class="text-white">Mostrando registros del 0 al 0 de un total de 0 registros',
			sInfoFiltered: '<p class="text-white">(filtrado de un total de _MAX_ registros)',
			sInfoPostFix: '<p class="text-white">',
			sSearch: '<p class="text-white">Buscar:',
			sUrl: '<p class="text-white">',
			sInfoThousands: '<p class="text-white">,',
			sLoadingRecords: '<p class="text-primary">Cargando...',
			oPaginate: {
				sFirst: '<p class="text-white">Primero',
				sLast: '<p class="text-white">Último',
				sNext: '<p class="text-white">Siguiente',
				sPrevious: '<p class="text-white">Anterior'
			},
			oAria: {
				sSortAscending: '<p class="text-white">: Activar para ordenar la columna de manera ascendente',
				sSortDescending: '<p class="text-white">: Activar para ordenar la columna de manera descendente'
			}
		}
	});

	// Inventario Libros
	var table = $('#tableBooks').DataTable({
		columnDefs: [
			{ targets: [ 3 ], visible: false, searchable: true },
			{ targets: [ 4 ], visible: false, searchable: true },
			{ targets: [ 5 ], visible: false, searchable: true },
			{ targets: [ 7 ], visible: false, searchable: true },
			{ targets: [ 10 ], visible: false, searchable: true },
			{ targets: [ 12 ], visible: false, searchable: true },
			{
				render: function(data, type, row) {
					return data + ' (' + row[5] + ')';
				},
				targets: 2
			}
		],
		scrollY: 350,
		scrollX: true,
		//stateSave: false,
		language: {
			sProcessing: '<p class="text-white">Procesando...',
			sLengthMenu: '<p class="text-white">Mostrar _MENU_ registros',
			sZeroRecords: '<p class="text-primary">No se encontraron resultados',
			sEmptyTable: '<p class="text-primary">Ningún dato disponible en esta tabla',
			sInfo: '<p class="text-white">Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros',
			sInfoEmpty: '<p class="text-white">Mostrando registros del 0 al 0 de un total de 0 registros',
			sInfoFiltered: '<p class="text-white">(filtrado de un total de _MAX_ registros)',
			sInfoPostFix: '<p class="text-white">',
			sSearch: '<p class="text-white">Buscar:',
			sUrl: '<p class="text-white">',
			sInfoThousands: '<p class="text-white">,',
			sLoadingRecords: '<p class="text-primary">Cargando...',
			oPaginate: {
				sFirst: '<p class="text-white">Primero',
				sLast: '<p class="text-white">Último',
				sNext: '<p class="text-white">Siguiente',
				sPrevious: '<p class="text-white">Anterior'
			},
			oAria: {
				sSortAscending: '<p class="text-white">: Activar para ordenar la columna de manera ascendente',
				sSortDescending: '<p class="text-white">: Activar para ordenar la columna de manera descendente'
			}
		}
	});

	// Add event listener for opening and closing details
	$('#tableBooks tbody').on('click', 'th', function() {
		function format(d) {
			// `d` is the original data object for the row
			return (
				'<div class="row text-primary"><div class="col-3 offset-1"><table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">' +
				'<tr>' +
				'<td>Autor:</td>' +
				'<td>' +
				d[3] +
				'</td>' +
				'</tr>' +
				'<tr>' +
				'<td>Editorial:</td>' +
				'<td>' +
				d[4] +
				'</td>' +
				'</tr>' +
				'</table></div>' +
				'<div class="col-3"> <table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">' +
				'<tr>' +
				'<td>Año de edición:</td>' +
				'<td>' +
				d[5] +
				'</td>' +
				'</tr>' +
				'<tr>' +
				'<td>Materia:</td>' +
				'<td>' +
				d[7] +
				'</td>' +
				'</tr>' +
				'</table></div>' +
				'<div class="col-3"> <table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">' +
				'<tr>' +
				'<td>Fecha de ingreso:</td>' +
				'<td>' +
				d[10] +
				'</td>' +
				'</tr>' +
				'<tr>' +
				'<td>Observaciones:</td>' +
				'<td>' +
				d[12] +
				'</td>' +
				'</tr>' +
				'</table></div></div>'
			);
		}
		var tr = $(this).closest('tr');
		var row = table.row(tr);

		if (row.child.isShown()) {
			// This row is already open - close it
			row.child.hide();
			tr.removeClass('shown');
		} else {
			// Open this row
			row.child(format(row.data())).show();
			tr.addClass('shown');
		}
	});
});

// DELETE BOOK
function deleteBook(book, name, year) {
	alertify
		.confirm(
			'Eliminando...',
			'Seguro que desea eliminar ' + name + '(' + year + ') ???',
			function() {
				location.href = '/deleteInv/' + book;
				//alertify.success('Ok');
			},
			function() {
				alertify.error('Cancelado');
			}
		)
		.set({ transition: 'zoom' });
}

// deleteRecordTCM
function deleteRecordTCM(code, description, marca) {
	alertify
		.confirm(
			'Eliminando...',
			'Seguro que desea eliminar ' + description + '(' + marca + ') ???',
			function() {
				location.href = '/deleteRecordTCM/' + code;
				//alertify.success('Ok');
			},
			function() {
				alertify.error('Cancelado');
			}
		)
		.set({ transition: 'zoom' });
}

// DELETE AUDIOVISUAL
function deleteAudiovisual(code, description) { // funcion para eliminar un elemento de audiovisual
	alertify
		.confirm( // llamado al metodo confirm de la libreria alertify de javaScript
			'Eliminando...', // leyenda en la parte superior de la ventana de confirmacion
			'Seguro que desea eliminar ' + description + '(' + code + ') ???', //leyenda en la parte superior
			function() { // llamado a la primer funcion del metodo confirm que corresponde a 'aceptar'
				location.href = '/deleteAudiovisual/' + code; // redireccionamiento a la ruta en donde su funcion de python realiza la eliminacion del elemento de audiovisual
			},
			function() { // llamado a la segunda funcion del metodo confirm que corresponde a 'cancelar'
				alertify.error('Cancelado'); // impresion de una alerta de error con la leyenda 'Cancelado'
			}
		)
		.set({ transition: 'zoom' }); // se define el tipo de animacion al abrirse la ventana
}

// DELETE LIBRARY
function deleteProjector(code, description) { // funcion para eliminar un elemento de biblioteca
	alertify
		.confirm( // llamado al metodo confirm de la libreria alertify de javaScript
			'Eliminando...', // leyenda en la parte superior de la ventana de confirmacion
			'Seguro que desea eliminar ' + description + '(' + code + ') ???', //leyenda en la parte superior
			function() { // llamado a la primer funcion del metodo confirm que corresponde a 'aceptar'
				location.href = '/deleteProjector/' + code; // redireccionamiento a la ruta en donde su funcion de python realiza la eliminacion del elemento de audiovisual
			},
			function() { // llamado a la segunda funcion del metodo confirm que corresponde a 'cancelar'
				alertify.error('Cancelado'); // impresion de una alerta de error con la leyenda 'Cancelado'
			}
		)
		.set({ transition: 'zoom' }); // se define el tipo de animacion al abrirse la ventana
}

// DELETE LIBRARY
function deleteLibrary(code, description) {
	alertify
		.confirm(
			'Eliminando...',
			'Seguro que desea eliminar ' + description + '(' + code + ') ???',
			function() {
				location.href = '/deleteLibrary/' + code;
				//alertify.success('Ok');
			},
			function() {
				alertify.error('Cancelado');
			}
		)
		.set({ transition: 'zoom' });
}

// DELETE VISITOR
function deleteVisitor(code, name) {
	alertify
		.confirm(
			'Eliminando...',
			'Seguro que desea eliminar ' + name + '(' + code + ') ???',
			function() {
				location.href = '/deleteVisitor/' + code;
				//alertify.success('Ok');
			},
			function() {
				alertify.error('Cancelado');
			}
		)
		.set({ transition: 'zoom' });
}

// LIBERACION DE LIBROS
function deliveryBooks(ruta, book) {
	alertify
		.confirm(
			'Liberando...',
			'Seguro de querer liberar "' + book + '" ???',
			function() {
				location.href = ruta;
			},
			function() {
				alertify.error('Cancelado');
			}
		)
		.set({ transition: 'zoom' });
}

// LIBERACION DE MOBILIARIO
function deliveryMobiliario(ruta) {
	alertify
		.confirm(
			'Liberando...',
			'Seguro de querer liberar el préstamo ???',
			function() {
				location.href = ruta;
			},
			function() {
				alertify.error('Cancelado');
			}
		)
		.set({ transition: 'zoom' });
}

// LIBERACION DE PROYECTORES
function deliveryProjectors(codeProjector, codeRecord) {
	alertify
		.confirm(
			'Liberando...',
			'Seguro de querer liberar el proyector ???',
			function() {
				location.href = '/deliveryProjector/' + codeProjector + '/' + codeRecord;
			},
			function() {
				alertify.error('Cancelado');
			}
		)
		.set({ transition: 'zoom' });
}

// LIBERACION DE RESERVACION AUDIOVISUAL
function deliveryAudiovisual(codeReservation) {
	alertify
		.confirm(
			'Liberando...',
			'Seguro de querer liberar la sala audiovisual ???',
			function() {
				location.href = '/deliveryAudiovisual/' + codeReservation;
			},
			function() {
				alertify.error('Cancelado');
			}
		)
		.set({ transition: 'zoom' });
}

// GENERAL CANCEL MESSAGE
async function cerrar() {
	alertify.error('Cancelado');
}

// IMPRESION DE CONTENEDOR
function imprimirDiv(content) {
	var restorePage = document.body.innerHTML;
	var printContent = document.getElementById(content).innerHTML;
	document.body.innerHTML = printContent;
	window.print();
	document.body.innerHTML = restorePage;
}

// SALIR DEL SISTEMA
function exit() {
	alertify
		.confirm(
			'Saliendo...',
			'Seguro que desea salir ???',
			function() {
				location.href = '/';
			},
			function() {
				alertify.error('Cancelado');
			}
		)
		.set({ transition: 'zoom' });
}
