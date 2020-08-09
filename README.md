# proyecto-modular
Aqui se estara trabajando el proceso de desarrollo de esta aplicacion, cada actualizacion, cada mejora se recomienda modificar este documento (en caso de ser necesario).

## Metodologia de trabajo
Al ser un proyecto de python que secuencialmente va a ir necesitando nuevos modulos y maneras de documentarlos se designara el patron de desarrollo siguiente:
- Para el proyecto con notebooks se usara el patron << [sugerido aqui](https://stackoverflow.com/a/38192558)>>
- Para la estructura del proyecto se usara la jerarquia siguiente: 

    project/
        common/
            files-used-in-common-modules.ext
        data/
            csv.csv
            images.img
            binary-files.bin
        docs/
            documentation.docs
        notebooks/
            module-name.ipynb
        proyect/
            python-files.py
        testing-algorithms/
            python-test.py

+ common/
    + Aqui se pondran los archivos que se usaran de manera publica por distintos modulos durante el proyecto
+ data/
    + Aqui se asignaran los datos requeridos por los modulos para funcionar de manera especializada, ya sean bases de datos, archivos binarios, archivos de configuracion, etc...
+ docs/
    + Aqui se guardara la documentacion que se vaya generando a lo largo del proyecto
+ notebooks/
    + Ciertos modulos requieren una introduccion previa para entender el funcionamiento, en forma de notas ipynb los guardaremos aqui. [Metodologia](#metodologia-de-trabajo)
+ proyect/
    + Aqui estara la jerarquia del proyecto en cuestion
+ testing-algorithms/
    + Aqui iran todas las pruebas unitarias de los modulos para verificar que funcionen siempre correctamente

## Etapa 1
Desarrollar un sistema computacional de visión artificial que analice un video de un entorno con características controladas (fácilmente clasificables). Durante el video, aparecerán nuevas características debido a que la cámara está siguiendo una trayectoria , así mismo, desaparecerán las más antiguas. Si la trayectoria regresa a mostrar características que ya habían sido detectadas, el sistema deberá ser capaz de reconocerlas.

### Modulos:
![Requerimientos](docs/Stage1.svg?raw=true "Diagrama de modulos")