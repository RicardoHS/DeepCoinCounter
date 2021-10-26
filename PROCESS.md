A continuacion se detalla el proceso seguido en el desarrollo del proyecto.

# Journal

### Day 0

La motivación del proyecto viene dada en conjunto con [este tweet](https://twitter.com/AlexanderNL/status/1410253599502962692)
y la necesidad de hacer algun proyecto (util) de ML que no requiera
datos complicados ni mucho esfuerzo.

Al observar como buscaba calderilla en mi bote de monedas, se me ocurrió la idea.

### Day 1

Investigacion de proyectos parecidos. Tras una rapida busqueda parece que no
hay mucho trabajo al respecto. Un par de papers de dudosa procedencia
y un post de un proyecto muy similar pero que parece inacabado.

Tras la investigación de trabajo me planifico el mio. Usar tflite parece buena idea.
En la documentacion tienen un ejemplo detallado de como usarlo con modelos de object detection.
Sobre la app del movil, y tras un par de videos de resumen tengo dudas entre React Native y Flutter para. 
Tras un par de videos más, me decido por Flutter.

El trabajo comienza con la preparacion de los datos sinteticos. Si consigo generar
suficientes fondos distintos con imagenes de monedas, todo parece que el proyecto
puede acabar bien.

### Day 2

Tras terminar el notebook inicial y pasarlo a script (muy buena decision), comienzo
con el modelado en tflite en otro notebook. Pierdo el dia practicamente instalando
de nuevo CUDA, ya que el codigo en tflite es realmente corto pero el entrenamiento
dura demasiado en CPU. [Tweet mio al respecto](https://twitter.com/RHortelanoS/status/1427338129623724038)

### Day 3

Tras instalar CUDA, las iteracciones de entrenamiento son mucho más rapidas y consigo
darme cuenta (al usar datos reales) de que voy a tener que usar dos modelos. Uno para 
detectar monedas (facil con datos sinteticos) y otro para clasificar las monedas (dificil
con datos sinteticos y que va a necesitar de etiquetar datos reales).

Como ya tengo un modelo que puede ser probado en Flutter y no quiero parar a etiquetar datos
decido seguir con el desarrollo y comenzar a mirar docu de Flutter. Lo más seguro es que con
el modelo de object detection se puede hacer una herramienta para etiquetar monedas
reales mucho mas facil.

### Day 4

Dia completo de empaparse de Flutter. Mirar la documentacion, hacer las apps de prueba
y terminar probando el pluggin de camara. Parece que el desarrollo de la app se puede
complicar mas de lo esperado. El framework es sencillo, muy compartimentado y si tienes
conocimientos previos de diseños de arquitectura de software es más facil de entender.
Por contra, el plugin no tiene casi docu, asi que queda pendiente un par de recursos
externos para entenderlo bien. 

 - [1](https://flutter.dev/docs/cookbook/plugins/picture-using-camera)
 - [2](https://medium.com/geekculture/build-a-camera-app-flutter-in-app-camera-825b829fe138)
 - [3](https://www.youtube.com/watch?v=boWJcIL1rHc)

### Day 5

Empiezo a escribir esta documentacion. Me puede servir para un post en el blog a futuro.
Fué un dia tranquilo.

### Day 6

Encuentro este proyecto que se parece al mio. https://medium.com/@sorenlind/a-deep-convolutional-denoising-autoencoder-for-image-classification-26c777d3b88e
