// animation bg

let canva = document.querySelector('canvas')

canva.width = window.innerWidth
canva.height = window.innerHeight

let c = canva.getContext('2d')

function Circle(x, y, dx, dy, radius) {
    this.x = x
    this.y = y
    this.dx = dx
    this.dy = dy
    this.radius = radius

    this.draw = function () {
        c.beginPath()
        c.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false)
        c.strokeStyle = 'rgb(167, 139, 250)'

        c.shadowColor = 'rgb(167, 200, 250)'
        c.shadowBlur = 15
        c.shadowOffsetX = 0
        c.shadowOffsetY = 0
        c.stroke()
    }

    this.update = function () {
        if (this.x > innerWidth || this.x < 0) {
            this.dx = -this.dx
        }

        if (this.y > innerHeight || this.y < 0) {
            this.dy = -this.dy
        }
        this.x += this.dx
        this.y += this.dy
        this.draw()
    }
}

let arr = []
for (let i = 0; i < 100; i++) {
    let x = Math.floor(Math.random() * innerWidth)
    let dx = ((Math.random() - 0.5))
    let y = Math.floor(Math.random() * innerHeight)
    let dy = ((Math.random() - 0.5))
    let radius = Math.floor(Math.random() * 10) + 5

    arr.push(new Circle(x, y, dx != 0 ? dx : dx + 1, dy != 0 ? dy : dy + 1, radius))
}

function animate() {
    requestAnimationFrame(animate)
    c.clearRect(0, 0, innerWidth, innerHeight)

    for (let i of arr) {
        i.update()
    }
}

animate()