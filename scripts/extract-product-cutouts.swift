#!/usr/bin/env swift
import AppKit
import CoreImage
import CoreImage.CIFilterBuiltins
import Vision

let arguments = CommandLine.arguments
if arguments.count != 3 {
    fputs("usage: extract-product-cutouts.swift INPUT OUTPUT\n", stderr)
    exit(2)
}

let inputURL = URL(fileURLWithPath: arguments[1])
let outputURL = URL(fileURLWithPath: arguments[2])
guard let input = CIImage(contentsOf: inputURL) else {
    fputs("cannot load input\n", stderr)
    exit(3)
}

let request = VNGenerateForegroundInstanceMaskRequest()
let handler = VNImageRequestHandler(ciImage: input)
try handler.perform([request])
guard let observation = request.results?.first else {
    fputs("no foreground mask\n", stderr)
    exit(4)
}
let maskBuffer = try observation.generateScaledMaskForImage(
    forInstances: observation.allInstances,
    from: handler
)
let mask = CIImage(cvPixelBuffer: maskBuffer)
let clear = CIImage(color: CIColor.clear).cropped(to: input.extent)
let blend = CIFilter.blendWithMask()
blend.inputImage = input
blend.backgroundImage = clear
blend.maskImage = mask

guard let output = blend.outputImage else {
    fputs("cannot composite output\n", stderr)
    exit(5)
}
let context = CIContext(options: [.useSoftwareRenderer: false])
let colorSpace = CGColorSpace(name: CGColorSpace.sRGB)!
try context.writePNGRepresentation(
    of: output,
    to: outputURL,
    format: .RGBA8,
    colorSpace: colorSpace
)
print("CUTOUT_OK \(inputURL.lastPathComponent) -> \(outputURL.lastPathComponent) \(Int(output.extent.width))x\(Int(output.extent.height)) instances=\(observation.allInstances.count)")
