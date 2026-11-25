(function () {
  'use strict';
  const datos = window.DATOS_REVISION || {};
  const visor = window.visorBpmn;
  const $ = id => document.getElementById(id);
  const api = location.protocol.startsWith('http') && ['127.0.0.1', 'localhost'].includes(location.hostname);
  let seleccionado = { id: '', ref: '', nombre: 'Diagrama completo', tipo: 'diagrama' };
  let graficoAnterior = null;
  let observaciones = [];
  let pestana = 'detalle';

  function campo(titulo, valor) {
    if (!valor) return;
    const dl = document.createElement('dl'); dl.className = 'campo';
    const dt = document.createElement('dt'); dt.textContent = titulo;
    const dd = document.createElement('dd'); dd.textContent = valor;
    dl.append(dt, dd); $('detalle').append(dl);
  }
  function enlace(titulo, ruta) {
    if (!ruta) return;
    const p = document.createElement('p');
    const a = document.createElement('a'); a.href = ruta; a.textContent = titulo;
    p.append(a); $('detalle').append(p);
  }
  function enlaceDocumento(titulo, nombre) {
    if (!nombre) return;
    const p = document.createElement('p');
    const boton = document.createElement('button');
    boton.className = 'enlace-fuente';
    boton.textContent = titulo;
    boton.onclick = () => abrirFuente({
      titulo, ruta: datos.modelo.slice(0, datos.modelo.lastIndexOf('/') + 1) + nombre
    });
    p.append(boton); $('detalle').append(p);
  }
  function mostrarFuentes() {
    if (seleccionado.categoria !== 'elemento') return;
    const fuentes = (datos.fuentes_visor || {})[seleccionado.ref] || [];
    const h = document.createElement('h2'); h.className = 'titulo-fuentes'; h.textContent = 'Documentos de sustento';
    $('detalle').append(h);
    if (!fuentes.length) {
      const p = document.createElement('p'); p.className = 'vacio';
      p.textContent = 'Ubicación precisa pendiente: falta registrar archivo y página o fragmento para esta caja.';
      $('detalle').append(p);
    }
    for (const fuente of fuentes) {
      const p = document.createElement('p');
      const boton = document.createElement('button'); boton.className = 'enlace-fuente';
      boton.textContent = `${fuente.titulo}${fuente.pagina ? ' · p. ' + fuente.pagina : ''}${fuente.ubicacion ? ' · ' + fuente.ubicacion : ''}`;
      boton.onclick = () => abrirFuente(fuente);
      p.append(boton);
      if (fuente.consulta || fuente.vigencia) {
        const meta = document.createElement('small');
        meta.className = 'metadatos-fuente';
        meta.textContent = [fuente.consulta && `Consulta: ${fuente.consulta}`, fuente.vigencia && `Vigencia: ${fuente.vigencia}`].filter(Boolean).join(' · ');
        p.append(meta);
      }
      $('detalle').append(p);
    }
  }
  function abrirFuente(fuente) {
    const pdf = fuente.ruta.toLowerCase().endsWith('.pdf');
    const ruta = '/' + fuente.ruta.split('/').map(encodeURIComponent).join('/');
    const destino = pdf
      ? ruta + '#' + [fuente.pagina ? 'page=' + fuente.pagina : '', fuente.fragmento ? 'search=' + encodeURIComponent(fuente.fragmento) : ''].filter(Boolean).join('&')
      : '/ver-fuente?ruta=' + encodeURIComponent(fuente.ruta) + '&fragmento=' + encodeURIComponent(fuente.fragmento || '');
    $('titulo-fuente').textContent = `${fuente.titulo}${fuente.pagina ? ' · página ' + fuente.pagina : ''}${fuente.ubicacion ? ' · ' + fuente.ubicacion : ''}`;
    $('fragmento-fuente').textContent = fuente.fragmento
      ? `Pasaje a consultar: «${fuente.fragmento}». El resaltado dentro del PDF depende del visor del navegador.`
      : '';
    $('marco-fuente').src = destino;
    $('abrir-fuente-externa').href = destino;
    $('dialogo-fuente').showModal();
  }
  function nodoArbol(nodo) {
    const li = document.createElement('li');
    const nombre = `${nodo.codigo} · ${nodo.nombre}`;
    const destino = nodo.modelo || nodo.indice;
    if (nodo.hijos?.length) {
      const detalles = document.createElement('details');
      const sumario = document.createElement('summary'); sumario.textContent = nombre;
      detalles.append(sumario);
      if (destino) {
        const a = document.createElement('a'); a.href = destino;
        a.textContent = nodo.modelo ? 'Abrir diagrama' : 'Abrir índice';
        if (nodo.modelo === '/' + datos.modelo) a.setAttribute('aria-current', 'page');
        detalles.append(a);
      }
      const ul = document.createElement('ul');
      nodo.hijos.forEach(h => ul.append(nodoArbol(h)));
      detalles.append(ul); li.append(detalles);
      if (nodo.codigo === 'Nivel 0' || (datos.codigo && (datos.codigo === nodo.codigo || datos.codigo.startsWith(nodo.codigo + '.')))) detalles.open = true;
    } else {
      const a = document.createElement('a'); a.textContent = nombre;
      if (destino) a.href = destino;
      if (nodo.modelo === '/' + datos.modelo) a.setAttribute('aria-current', 'page');
      li.append(a);
    }
    return li;
  }
  async function cargarArbol() {
    if (!api) return;
    try {
      const r = await fetch('/api/arbol');
      if (!r.ok) throw Error('HTTP ' + r.status);
      const ul = document.createElement('ul'); ul.append(nodoArbol(await r.json()));
      $('arbol-procesos').replaceChildren(ul);
    } catch (e) { $('arbol-procesos').textContent = 'No se pudo cargar el árbol: ' + e.message; }
  }
  function mostrarDetalle() {
    $('titulo-seleccion').textContent = seleccionado.numero ? `${seleccionado.numero} · ${seleccionado.nombre || seleccionado.ref}` : (seleccionado.nombre || seleccionado.ref);
    $('subtitulo-seleccion').textContent = seleccionado.ref || datos.codigo || '';
    $('detalle').replaceChildren();
    if (seleccionado.tipo === 'diagrama') {
      campo('Proceso', datos.codigo);
      campo('Descripción', 'Selecciona una caja o una flecha para consultar sus datos y registrar una observación.');
    } else if (seleccionado.categoria === 'flujo') {
      campo('Conexión', `${seleccionado.origen} → ${seleccionado.destino}`);
      campo('Tipo', seleccionado.claseFlujo);
      campo('Condición', seleccionado.condicion);
      campo('Descripción', seleccionado.nombre);
      campo('Sustento específico', seleccionado.fuente || 'Pendiente de documentar para esta conexión.');
    } else {
      for (const [titulo, clave] of [['ID de tabla','ref'],['Responsable','carril'],['Participante','pool'],['Tipo','tipo'],['Plazo','plazo'],['Disparador','disparador'],['Documentos','documentos'],['Anotación','anotacion'],['Clase de conocimiento','clase'],['Fuente registrada','fuente']]) campo(titulo, seleccionado[clave]);
      if (seleccionado.destino) enlace(
        seleccionado.destino_tipo === 'diagrama' ? 'Abrir diagrama del proceso interior' : 'Abrir índice del proceso interior',
        seleccionado.destino,
      );
    }
    mostrarFuentes();
    enlaceDocumento('Ver tabla fuente', datos.tabla);
    enlaceDocumento('Ver sustento del proceso', datos.sustento);
  }
  function cambiarPestana(nombre) {
    pestana = nombre;
    for (const clave of ['detalle', 'observaciones']) {
      $(clave).hidden = clave !== nombre;
      $(`tab-${clave}`).classList.toggle('activa', clave === nombre);
    }
    if (nombre === 'observaciones') mostrarObservaciones();
  }
  function seleccionar(elemento) {
    if (graficoAnterior) graficoAnterior.classList.remove('revision-seleccionado');
    graficoAnterior = null;
    if (!elemento) {
      seleccionado = { id: '', ref: '', nombre: 'Diagrama completo', tipo: 'diagrama' };
    } else {
      const id = elemento.id;
      const nodo = (datos.elementos || {})[id];
      const flujo = (datos.flujos || {})[id];
      seleccionado = nodo ? { ...nodo, id, categoria: 'elemento' } : flujo ? {
        id, ref: `${flujo.origen} → ${flujo.destino}`, nombre: flujo.nombre || flujo.condicion || 'Flujo',
        categoria: 'flujo', claseFlujo: flujo.tipo, ...flujo
      } : { id, ref: id, nombre: elemento.businessObject?.name || elemento.type || id, categoria: 'elemento' };
      graficoAnterior = visor.get('elementRegistry').getGraphics(id);
      if (graficoAnterior) graficoAnterior.classList.add('revision-seleccionado');
    }
    mostrarDetalle();
    if (pestana === 'observaciones') mostrarObservaciones();
  }
  // Las observaciones en HTML (ya saneadas en el servidor) se muestran aquí como texto plano, sin interpretar etiquetas.
  function textoVisible(o) {
    if (o.formato !== 'html') return o.texto;
    return new DOMParser().parseFromString(o.texto, 'text/html').body.textContent || '';
  }
  function mostrarObservaciones() {
    const lista = $('lista-observaciones'); lista.replaceChildren();
    const elegidas = seleccionado.id ? observaciones.filter(o => o.elemento === seleccionado.id) : observaciones;
    $('cuenta-observaciones').textContent = `${elegidas.length} ${seleccionado.id ? 'en esta selección' : 'en el modelo'} · ${observaciones.filter(o => o.estado !== 'RESUELTA').length} abiertas`;
    if (!elegidas.length) {
      const p = document.createElement('p'); p.className = 'vacio'; p.textContent = 'No hay observaciones para esta selección.'; lista.append(p);
    }
    for (const o of elegidas) {
      const tarjeta = document.createElement('div'); tarjeta.className = 'obs';
      const cab = document.createElement('small'); cab.textContent = `${o.estado} · ${o.referencia || datos.codigo} · ${o.autor} · ${o.fecha.slice(0,10)}`;
      const cuerpo = document.createElement('p'); cuerpo.textContent = textoVisible(o);
      tarjeta.append(cab, cuerpo);
      if (!seleccionado.id && o.elemento) {
        const ir = document.createElement('button'); ir.textContent = 'Ver elemento';
        ir.onclick = () => seleccionar(visor.get('elementRegistry').get(o.elemento));
        tarjeta.append(ir);
      }
      if (api && o.estado !== 'RESUELTA') {
        const boton = document.createElement('button'); boton.textContent = 'Marcar resuelta';
        boton.onclick = () => actualizar(o.id, 'RESUELTA'); tarjeta.append(boton);
      }
      lista.append(tarjeta);
    }
  }
  async function cargar() {
    if (!api) { $('estado-guardado').textContent = 'Para guardar, abre esta vista mediante el servidor local de revisión.'; return; }
    try {
      const r = await fetch(`/api/observaciones?modelo=${encodeURIComponent(datos.modelo)}`);
      if (!r.ok) throw Error(`HTTP ${r.status}`);
      observaciones = (await r.json()).observaciones || [];
      $('estado-guardado').textContent = 'Observaciones guardadas en el repositorio local.';
      mostrarObservaciones();
    } catch (e) { $('estado-guardado').textContent = `No se pudo cargar: ${e.message}`; }
  }
  async function enviar() {
    const texto = $('texto-observacion').value.trim();
    if (!texto) { $('estado-guardado').textContent = 'Escribe la observación.'; return; }
    if (!api) { $('estado-guardado').textContent = 'Inicia el servidor local para guardar.'; return; }
    try {
      const r = await fetch('/api/observaciones', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({
        modelo:datos.modelo, elemento:seleccionado.id, referencia:seleccionado.ref || datos.codigo,
        texto, autor:$('autor-observacion').value.trim() || 'Equipo'
      })});
      if (!r.ok) throw Error((await r.json()).error || `HTTP ${r.status}`);
      $('texto-observacion').value = ''; await cargar();
    } catch (e) { $('estado-guardado').textContent = `No se pudo guardar: ${e.message}`; }
  }
  async function actualizar(id, estado) {
    try {
      const r = await fetch('/api/observaciones', { method:'PATCH', headers:{'Content-Type':'application/json'}, body:JSON.stringify({modelo:datos.modelo,id,estado}) });
      if (!r.ok) throw Error((await r.json()).error || `HTTP ${r.status}`);
      await cargar();
    } catch (e) { $('estado-guardado').textContent = `No se pudo actualizar: ${e.message}`; }
  }
  $('tab-detalle').onclick = () => cambiarPestana('detalle');
  $('abrir-arbol').onclick = () => $('dialogo-arbol').showModal();
  $('cerrar-arbol').onclick = () => $('dialogo-arbol').close();
  $('cerrar-fuente').onclick = () => { $('dialogo-fuente').close(); $('marco-fuente').src = 'about:blank'; };
  $('tab-observaciones').onclick = () => cambiarPestana('observaciones');
  $('ver-diagrama').onclick = () => seleccionar(null);
  $('agregar-observacion').onclick = enviar;
  $('exportar-observaciones').onclick = () => {
    const abiertas = observaciones.filter(o => o.estado !== 'RESUELTA');
    const paquete = {
      proceso: datos.codigo, modelo: datos.modelo,
      instruccion: 'Revisar estas observaciones contra la tabla y el sustento. Proponer cambios; no asignar validación institucional.',
      observaciones: abiertas.map(o => ({
        ...o, elemento_modelo: (datos.elementos || {})[o.elemento] || (datos.flujos || {})[o.elemento] || null
      }))
    };
    const enlace = document.createElement('a');
    enlace.href = URL.createObjectURL(new Blob([JSON.stringify(paquete, null, 2)], { type: 'application/json' }));
    enlace.download = `${datos.codigo || 'modelo'}-observaciones-abiertas.json`;
    enlace.click(); setTimeout(() => URL.revokeObjectURL(enlace.href), 1000);
  };
  $('volver-padre').hidden = !datos.padre;
  if (datos.padre) $('volver-padre').href = datos.padre;
  const canvas = visor.get('canvas');
  $('ajustar').onclick = () => canvas.zoom('fit-viewport');
  $('acercar').onclick = () => canvas.zoom(Math.min(4, canvas.zoom() * 1.2));
  $('alejar').onclick = () => canvas.zoom(Math.max(0.1, canvas.zoom() / 1.2));
  $('c').addEventListener('wheel', e => {
    e.preventDefault(); e.stopImmediatePropagation();
    const rect = $('c').getBoundingClientRect();
    const escala = Math.max(0.1, Math.min(4, canvas.zoom() * (e.deltaY < 0 ? 1.12 : 1/1.12)));
    canvas.zoom(escala, { x: e.clientX - rect.left, y: e.clientY - rect.top });
  }, { passive:false, capture:true });
  visor.get('eventBus').on('element.click', e => seleccionar(e.element.labelTarget || e.element));
  $('c').addEventListener('click', e => {
    const forma = e.target.closest?.('.djs-shape[data-element-id]');
    if (!forma) return;
    const nodo = (datos.elementos || {})[forma.getAttribute('data-element-id')];
    if (!nodo?.tipo?.startsWith('subproceso')) return;
    const rect = forma.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width;
    const y = (e.clientY - rect.top) / rect.height;
    if (x < 0.32 || x > 0.68 || y < 0.64) return;
    e.preventDefault(); e.stopImmediatePropagation();
    seleccionar(visor.get('elementRegistry').get(forma.getAttribute('data-element-id')));
  }, true);
  mostrarDetalle(); cargar(); cargarArbol();
})();
