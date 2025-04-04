import sys

def check_python_version():
    version = sys.version
    return version.split(" ")[0].strip()

try :
    if check_python_version() == "3.8.0":
        raise RuntimeError(f"Version mismatch: use 2nd venv to run this script. {check_python_version()} will not work")
    # Write from here .
    import albumentations as A
    import cv2, os, numpy as np
    from PIL import Image

    class_map = ['Cap1', 'Cap2', 'Cap3', 'Cap4', 'MOSFET', 'Mov', 'Resestor', 'Resistor', 'Transformer', 'Ic', 'Diode', 'Cap6', 'Transistor', 'Potentiometer']

    transform = A.Compose([
        A.SmallestMaxSize(max_size=400, p=1.0),  # Resize smaller dimension to 400px while maintaining aspect ratio
        A.RandomCrop(width=int(400*0.8), height=int(400*0.8)),  # Crop 80% of the resized image
        # A.RandomCrop(width=450, height=450),
        A.HorizontalFlip(p=0.5),
        A.RandomBrightnessContrast(p=0.2)],
        bbox_params=A.BboxParams(format='yolo'))
    
    def transformer(transform, image, bboxes):
        transformed = transform(image=image, bboxes=bboxes)
        transformed_image = transformed['image']
        transformed_bboxes = transformed['bboxes']
        return transformed_image, transformed_bboxes

    def load_yolo_annotation(txt_path):
        classes_backup = []
        bboxes = []
        with open(txt_path, 'r') as f:
            bboxes = [(list(map(float ,line.strip().split()[1:])) + [int(line.strip().split()[0])]) for line in f]
            # for line in f:
            #     classes_backup.append(line.strip().split()[0])
            """
            # The below code wont work because if we iterate f for once then the file pointer will reach to the end 
            # and for 2nd line there wont be any lines left to read.
            //
            # classes_backup = [line.strip().split()[0] for line in f]
            # bboxes = [list(map(float, line.strip().split()[1:])) + [class_map[int(line.strip().split()[0])]] for line in f]
            """

        return bboxes

    # annotation_file = "../ann/Circuit-Board-Resistors-1-1024x753.txt"
    # bboxes, classes_backup = load_yolo_annotation(annotation_file)
    # image = cv2.imread("../img/Circuit-Board-Resistors-1-1024x753.jpg")
    # n_image, n_boxes = transformer(transform=transform, image=image, bboxes=bboxes)
    # for i in range((len(n_boxes))):
    #     print(f"{n_boxes[i]} {classes_backup[i]}")
    # sys.exit(0)

    def main():
        try:
            # Create output directories 
            os.makedirs("../augmented_img", exist_ok=True)
            os.makedirs("../augmented_ann", exist_ok=True)

            txt_files = os.listdir("../ann")
            txt_files.remove("classes.txt")
            img_files = os.listdir("../img")
            count = 0
            total = len(img_files)
            for i in range(len(txt_files)):
                if txt_files[i].rsplit('.', 1)[0] == img_files[i].rsplit('.', 1)[0]:
                    print(f"{txt_files[i].rsplit('.', 1)[0]} : {img_files[i].rsplit('.', 1)[0]}")
                    bbboxes = load_yolo_annotation(os.path.join("../ann", txt_files[i]))
                    # image = cv2.imread(os.path.join("../img", img_files[i]))
                    image = np.array(Image.open(os.path.join("../img", img_files[i])))
                    new_image, new_txt = transformer(transform=transform, image=image, bboxes=bbboxes)
                    # After getting transformed image and annotation. Lets save it
                    aug_filename = f"{img_files[i].rsplit('.', 1)[0]}_aug_{count}"
                    new_img_path = os.path.join("../augmented_img", f"{aug_filename}.jpg")
                    new_txt_path  = os.path.join("../augmented_ann", f"{aug_filename}.txt")
                    cv2.imwrite(new_img_path, new_image)
                    with open(new_txt_path, 'w') as f:
                        for bbox in range(len(new_txt)):
                            f.write(f"{int(new_txt[bbox][4])} {new_txt[bbox][0]} {new_txt[bbox][1]} {new_txt[bbox][2]} {new_txt[bbox][3]}\n")

                    count += 1
                    print(f"Done {count} / {total}")

        except RuntimeError as e:
            print(f"Inner array {e}")
    if __name__ == "__main__":
        main()

except RuntimeError as e:
    print(e)
