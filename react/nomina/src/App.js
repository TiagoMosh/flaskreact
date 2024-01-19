import React, { useState, useEffect } from 'react';

import 'bootstrap/dist/css/bootstrap.min.css';
import { Modal, ModalBody, ModalFooter, ModalHeader } from 'reactstrap';
import axios from 'axios';


function App() {
  const [data, setData] = useState([]);
  const [modalInsertar, setModalInsertar] = useState(false);
  const [modalEditar, setModalEditar] = useState(false);
  const [modalEliminar, setModalEliminar] = useState(false);
  const [modalRealizar, setModalRealizar] = useState(false);
  const [frameworkSeleccionado, setFrameworkSeleccionado] = useState({
    id: '',
    documento: '',
    nombre: '',
    sexo: '',
    telefono: '',
    fechaingreso: '',
    fechanacimiento: '',
    cargo: '',
    salarioinicial: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFrameworkSeleccionado((prevState) => ({
      ...prevState,
      [name]: value
    }));
    console.log(frameworkSeleccionado);
  };

  const abrirCerrarModalInsertar = () => {
    setModalInsertar(!modalInsertar);
  };

  const abrirCerrarModalEditar = () => {
    setModalEditar(!modalEditar);
  };

  const abrirCerrarModalEliminar = () => {
    setModalEliminar(!modalEliminar);
  };
  const abrirCerrarModalRealizar = () => {
    setModalRealizar(!modalRealizar);
  };

  const peticionGet = async () => {
    const baseUrl = 'http://127.0.0.1:5000/empleados';
    try {
      const response = await axios.get(baseUrl);
      console.log(response.data);

      const empleados = response.data.empleados;
      if (Array.isArray(empleados)) {
        setData(empleados);
      } else {
        console.error('Los datos recibidos no son un array.');
      }
    } catch (error) {
      console.error(error);
    }
  };
  
  const peticionPost = async () => {
    const baseUrl = 'http://127.0.0.1:5000/empleados';
    var f = new FormData();
    f.append("documento", frameworkSeleccionado.documento);
    f.append("nombre", frameworkSeleccionado.nombre);
    f.append("sexo", frameworkSeleccionado.sexo);
    f.append("telefono", frameworkSeleccionado.telefono);
    f.append("fechaingreso", frameworkSeleccionado.fechaingreso);
    f.append("fechanacimiento", frameworkSeleccionado.fechanacimiento);
    f.append("cargo", frameworkSeleccionado.cargo);
    f.append("salarioinicial", frameworkSeleccionado.salarioinicial);
  
    try {
      const response = await axios.post(baseUrl, frameworkSeleccionado, { headers: { 'Content-Type': 'application/json' } });
      console.log(response.data);
  
      setData(data.concat(response.data));
      abrirCerrarModalInsertar();

      window.location.reload();
    } catch (error) {
      console.log(error);
    }
  };
  

  const peticionPut = async () => {
    const baseUrl = `http://127.0.0.1:5000/empleados/${frameworkSeleccionado.id}`;
  
    try {
      const response = await axios.put(baseUrl, {
        documento: frameworkSeleccionado.documento,
        nombre: frameworkSeleccionado.nombre,
        sexo: frameworkSeleccionado.sexo,
        telefono: frameworkSeleccionado.telefono,
        fechaingreso: frameworkSeleccionado.fechaingreso,
        fechanacimiento: frameworkSeleccionado.fechanacimiento,
        cargo: frameworkSeleccionado.cargo,
        salarioinicial: frameworkSeleccionado.salarioinicial
      });
      console.log(response.data);
      abrirCerrarModalEditar();
  
      await peticionGet();
    } catch (error) {
      console.log(error);
    }
  };
  


  const peticionDelete = async () => {
    const baseUrl = `http://127.0.0.1:5000/empleados/${frameworkSeleccionado.id}`;
    var f = new FormData();
    await axios.delete(baseUrl, f, { params: { id: frameworkSeleccionado.id } }).then(() => {
      setData(data.filter((framework) => framework.id !== frameworkSeleccionado.id));
      abrirCerrarModalEliminar();
    }).catch((error) => {
      console.log(error);
    });
  };
 ///acaaa


  const seleccionarFramework = (framework, caso) => {
    setFrameworkSeleccionado(framework);

    if (caso === "Editar") {
      abrirCerrarModalEditar();
    } else if (caso === "Eliminar") {
      abrirCerrarModalEliminar();
    }
    else if (caso === "Realizar") {
      abrirCerrarModalRealizar();
    }
  };

  useEffect(() => {
    peticionGet();
  }, []);

  return (
    <div style={{ textAlign: 'center' }}>
      <br />
      <button className="btn btn-success" onClick={() => abrirCerrarModalInsertar()}>Insertar empleado</button>
      <br /><br />
      <table className="table table-striped">
        <thead>
          <tr>
            <th>Id</th>
            <th>Documento</th>
            <th>Nombre</th>
            <th>Sexo</th>
            <th>Teléfono</th>
            <th>Fecha de ingreso</th>
            <th>Fecha de nacimiento</th>
            <th>Cargo</th>
            <th>Salario inicial</th>
          </tr>
        </thead>
        <tbody>
          {data.map((framework) => (
            <tr key={framework.id}>
              <td>{framework.id}</td>
              <td>{framework.documento}</td>
              <td>{framework.nombre}</td>
              <td>{framework.sexo}</td>
              <td>{framework.telefono}</td>
              <td>{framework.fechaingreso}</td>
              <td>{framework.fechanacimiento}</td>
              <td>{framework.cargo}</td>
              <td>{framework.salarioinicial}</td>
              <td>
                <button className="btn btn-primary" onClick={() => seleccionarFramework(framework, "Editar")}>Editar</button>
                {" "}
                <button className="btn btn-danger" onClick={() => seleccionarFramework(framework, "Eliminar")}>Eliminar</button>
                {" "}
                <button className="btn btn-success" onClick={() => seleccionarFramework(framework, "Realizar")}>Realizar nómina</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <Modal isOpen={modalInsertar}>
        <ModalHeader>Insertar Empleado</ModalHeader>
        <ModalBody>
          <div className="form-group">
            <label>Documento: </label>
            <br />
            <input type="text" className="form-control" name="documento" onChange={handleChange} />
            <br />
            <label>Nombre: </label>
            <br />
            <input type="text" className="form-control" name="nombre" onChange={handleChange} />
            <br />
            <label>Sexo: </label>
            <br />
            <input type="text" className="form-control" name="sexo" onChange={handleChange} />
            <br />
            <label>Teléfono: </label>
            <br />
            <input type="text" className="form-control" name="telefono" onChange={handleChange} />
            <br />
            <label>Fecha de ingreso: </label>
            <br />
            <input type="date" className="form-control" name="fechaingreso" onChange={handleChange} />
            <br />
            <label>Fecha de nacimiento: </label>
            <br />
            <input type="date" className="form-control" name="fechanacimiento" onChange={handleChange} />
            <br />
            <label>Cargo: </label>
            <br />
            <input type="text" className="form-control" name="cargo" onChange={handleChange} />
            <br />
            <label>Salario inicial: </label>
            <br />
            <input type="text" className="form-control" name="salarioinicial" onChange={handleChange} />
            <br />
          </div>
        </ModalBody>
        <ModalFooter>
          <button className="btn btn-primary" onClick={() => peticionPost()}>Insertar</button>
          {" "}
          <button className="btn btn-danger" onClick={() => abrirCerrarModalInsertar()}>Cancelar</button>
        </ModalFooter>
      </Modal>

      <Modal isOpen={modalEditar}>
        <ModalHeader>Editar </ModalHeader>
        <ModalBody>
          <div className="form-group">
            <label>Documento: </label>
            <br />
            <input type="text" className="form-control" name="documento" onChange={handleChange} value={frameworkSeleccionado && frameworkSeleccionado.documento} />
            <br />
            <label>Nombre: </label>
            <br />
            <input type="text" className="form-control" name="nombre" onChange={handleChange} value={frameworkSeleccionado && frameworkSeleccionado.nombre} />
            <br />
            <label>Sexo: </label>
            <br />
            <input type="text" className="form-control" name="sexo" onChange={handleChange} value={frameworkSeleccionado && frameworkSeleccionado.sexo} />
            <br />
            <label>Teléfono: </label>
            <br />
            <input type="text" className="form-control" name="telefono" onChange={handleChange} value={frameworkSeleccionado && frameworkSeleccionado.telefono} />
            <br />
            <label>Fecha de ingreso: </label>
            <br />
            <input type="date" className="form-control" name="fechaingreso" onChange={handleChange} value={frameworkSeleccionado && frameworkSeleccionado.fechaingreso} />
            <br />
            <label>Fecha de nacimiento: </label>
            <br />
            <input type="date" className="form-control" name="fechanacimiento" onChange={handleChange} value={frameworkSeleccionado && frameworkSeleccionado.fechanacimiento} />
            <br />
            <label>Cargo </label>
            <br />
            <input type="text" className="form-control" name="cargo" onChange={handleChange} value={frameworkSeleccionado && frameworkSeleccionado.cargo} />
            <br />
            <label>Salario inicial </label>
            <br />
            <input type="text" className="form-control" name="salarioinicial" onChange={handleChange} value={frameworkSeleccionado && frameworkSeleccionado.salarioinicial} />
            <br />
          </div>
        </ModalBody>
        <ModalFooter>
          <button className="btn btn-primary" onClick={() => peticionPut()}>Editar</button>
          {" "}
          <button className="btn btn-danger" onClick={() => abrirCerrarModalEditar()}>Cancelar</button>
        </ModalFooter>
      </Modal>

      <Modal isOpen={modalEliminar}>
        <ModalBody>
          ¿Estás seguro que deseas eliminar el empleado? {frameworkSeleccionado && frameworkSeleccionado.nombre}?
        </ModalBody>
        <ModalFooter>
          <button className="btn btn-danger" onClick={() => peticionDelete()}>Sí</button>
          <button className="btn btn-secondary" onClick={() => abrirCerrarModalEliminar()}>No</button>
        </ModalFooter>
      </Modal>
      <Modal isOpen={modalRealizar}>
        <ModalHeader>Realizar nómina</ModalHeader>
        <ModalBody>
          <div className="form-group">

            <label>Horas trabajadas: </label>
            <br />
            <input type="text" className="form-control" name="horas_trabajadas" onChange={handleChange} />
            <br />
            <label>Horas extras: </label>
            <br />
            <input type="text" className="form-control" name="horas_extras" onChange={handleChange} />
            <br />
            <label>Horas nocturnas </label>
            <br />
            <input type="text" className="form-control" name="horas_nocturnas" onChange={handleChange} />
            <br />
            <label>Horas dominicales: </label>
            <br />
            <input type="text" className="form-control" name="horas_dominicales" onChange={handleChange} />
            <br />
            <label>Comisiones: </label>
            <br />
            <input type="text" className="form-control" name="comisiones" onChange={handleChange} />
            <br />
            <label>Deducciones: </label>
            <br />
            <input type="text" className="form-control" name="deducciones" onChange={handleChange} />
            <br />
            <input type="text" className="form-control" name="salario_neto" onChange={handleChange} />
            <br />
            <label>Fecha emisión: </label>
            <br />
            <input type="date" className="form-control" name="fecha_emision" onChange={handleChange} />
            <br />
          </div>
          
        </ModalBody>
        <ModalFooter>
          <button className="btn btn-primary" onClick={() => peticionPost()}>Insertar</button>
          {" "}
          <button className="btn btn-danger" onClick={() => abrirCerrarModalRealizar()}>Cancelar</button>
        </ModalFooter>
      </Modal>
    </div>
  );
}

export default App;