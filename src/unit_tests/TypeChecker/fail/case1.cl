class Main inherits IO {
    main(): String {
        case "asd" of
            str : String => out_string(str);
            bruh : Object => out_string("is object");
        esac
    };
};